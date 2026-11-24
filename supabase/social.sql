-- =====================================================================
-- CURTIDAS, COMENTÁRIOS E COMPARTILHAMENTOS das páginas de certificação
-- Cole tudo no Supabase: SQL Editor > New query > Run. Pode rodar de novo
-- sem problema (o script é idempotente).
--
-- Segurança: os visitantes NÃO acessam as tabelas diretamente (RLS ligado
-- e sem políticas). Só conseguem chamar as funções abaixo, que validam os
-- dados e limitam abusos. A chave pública no site só permite isso.
--
-- Moderação: todo comentário entra com aprovado = false. Para publicar,
-- abra Table Editor > comentarios e marque "aprovado". Para responder,
-- escreva na coluna "resposta" (aparece com o selo "Instrutor").
-- =====================================================================

create table if not exists public.curtidas (
  cert        text not null,
  dispositivo uuid not null,
  criado      timestamptz not null default now(),
  primary key (cert, dispositivo)
);

-- "Minhas metas": quem salvou cada certificação (um registro por aparelho)
create table if not exists public.metas (
  cert        text not null,
  dispositivo uuid not null,
  criado      timestamptz not null default now(),
  primary key (cert, dispositivo)
);

create table if not exists public.compartilhamentos (
  id          bigint generated always as identity primary key,
  cert        text not null,
  canal       text not null,
  dispositivo uuid,
  criado      timestamptz not null default now()
);

create table if not exists public.comentarios (
  id          bigint generated always as identity primary key,
  cert        text not null,
  nome        text not null,
  texto       text not null,
  dispositivo uuid not null,
  aprovado    boolean not null default false,
  resposta    text,
  criado      timestamptz not null default now()
);

create index if not exists comentarios_cert_idx on public.comentarios (cert, aprovado, criado);
create index if not exists compart_cert_idx on public.compartilhamentos (cert, canal);
create index if not exists compart_disp_idx on public.compartilhamentos (dispositivo, criado);
create index if not exists coment_disp_idx on public.comentarios (dispositivo, criado);

alter table public.curtidas          enable row level security;
alter table public.metas             enable row level security;
alter table public.compartilhamentos enable row level security;
alter table public.comentarios       enable row level security;
revoke all on public.curtidas, public.metas, public.compartilhamentos, public.comentarios from anon, authenticated;

-- Código de certificação válido: "az-104", "ai-901", "ab-100"...
create or replace function public._cert_ok(p text) returns boolean
language sql immutable as $$ select p ~ '^[a-z]{2}-[0-9]{3}$' $$;

-- ---------------------------------------------------------------------
-- Números de todas as certificações (uma chamada só)
-- ---------------------------------------------------------------------
create or replace function public.contagens()
returns table (cert text, curtidas bigint, comentarios bigint, reposts bigint, compart bigint)
language sql stable security definer set search_path = public as $$
  with c as (
    select cert from curtidas
    union select cert from comentarios where aprovado
    union select cert from compartilhamentos
  )
  select c.cert,
    (select count(*) from curtidas x where x.cert = c.cert),
    (select count(*) from comentarios x where x.cert = c.cert and x.aprovado),
    (select count(*) from compartilhamentos x where x.cert = c.cert and x.canal = 'linkedin'),
    (select count(*) from compartilhamentos x where x.cert = c.cert and x.canal <> 'linkedin')
  from c;
$$;

-- ---------------------------------------------------------------------
-- Curtir / descurtir (uma curtida por aparelho). Devolve o total novo.
-- ---------------------------------------------------------------------
create or replace function public.curtir(p_cert text, p_dispositivo uuid, p_curtir boolean default true)
returns bigint
language plpgsql security definer set search_path = public as $$
begin
  if not _cert_ok(p_cert) then raise exception 'certificacao invalida'; end if;
  if p_curtir then
    insert into curtidas (cert, dispositivo) values (p_cert, p_dispositivo) on conflict do nothing;
  else
    delete from curtidas where cert = p_cert and dispositivo = p_dispositivo;
  end if;
  return (select count(*) from curtidas where cert = p_cert);
end $$;

-- ---------------------------------------------------------------------
-- Salvar / remover de "Minhas metas" (um por aparelho)
-- ---------------------------------------------------------------------
create or replace function public.salvar(p_cert text, p_dispositivo uuid, p_salvar boolean default true)
returns void
language plpgsql security definer set search_path = public as $$
begin
  if not _cert_ok(p_cert) then raise exception 'certificacao invalida'; end if;
  if p_salvar then
    insert into metas (cert, dispositivo) values (p_cert, p_dispositivo) on conflict do nothing;
  else
    delete from metas where cert = p_cert and dispositivo = p_dispositivo;
  end if;
end $$;

-- ---------------------------------------------------------------------
-- Registrar um compartilhamento (até 30 por aparelho por hora)
-- ---------------------------------------------------------------------
create or replace function public.compartilhar(p_cert text, p_canal text, p_dispositivo uuid)
returns void
language plpgsql security definer set search_path = public as $$
begin
  if not _cert_ok(p_cert) then raise exception 'certificacao invalida'; end if;
  if p_canal not in ('whatsapp','linkedin','telegram','x','facebook','email','link','nativo') then
    raise exception 'canal invalido';
  end if;
  if (select count(*) from compartilhamentos
      where dispositivo = p_dispositivo and criado > now() - interval '1 hour') >= 30 then
    return;
  end if;
  insert into compartilhamentos (cert, canal, dispositivo) values (p_cert, p_canal, p_dispositivo);
end $$;

-- ---------------------------------------------------------------------
-- Enviar comentário (fica pendente até você aprovar)
-- Limites: 3 por aparelho a cada 10 minutos e 15 por dia.
-- ---------------------------------------------------------------------
create or replace function public.comentar(p_cert text, p_nome text, p_texto text, p_dispositivo uuid)
returns bigint
language plpgsql security definer set search_path = public as $$
declare v_id bigint;
begin
  if not _cert_ok(p_cert) then raise exception 'certificacao invalida'; end if;
  p_nome := btrim(p_nome); p_texto := btrim(p_texto);
  if char_length(p_nome) not between 2 and 40 then raise exception 'nome invalido'; end if;
  if char_length(p_texto) not between 2 and 600 then raise exception 'texto invalido'; end if;
  if (select count(*) from comentarios where dispositivo = p_dispositivo and criado > now() - interval '10 minutes') >= 3
     or (select count(*) from comentarios where dispositivo = p_dispositivo and criado > now() - interval '1 day') >= 15 then
    raise exception 'limite de comentarios';
  end if;
  insert into comentarios (cert, nome, texto, dispositivo) values (p_cert, p_nome, p_texto, p_dispositivo)
  returning id into v_id;
  return v_id;
end $$;

-- ---------------------------------------------------------------------
-- Comentários aprovados de uma certificação (sem expor o aparelho)
-- ---------------------------------------------------------------------
create or replace function public.comentarios_de(p_cert text)
returns table (id bigint, nome text, texto text, resposta text, criado timestamptz)
language sql stable security definer set search_path = public as $$
  select id, nome, texto, resposta, criado from comentarios
  where cert = p_cert and aprovado order by criado asc limit 200;
$$;

-- Só estas funções ficam disponíveis para o site
revoke execute on all functions in schema public from public, anon, authenticated;
grant execute on function public.contagens()                            to anon, authenticated;
grant execute on function public.curtir(text, uuid, boolean)            to anon, authenticated;
grant execute on function public.compartilhar(text, text, uuid)         to anon, authenticated;
grant execute on function public.salvar(text, uuid, boolean)            to anon, authenticated;
grant execute on function public.comentar(text, text, text, uuid)       to anon, authenticated;
grant execute on function public.comentarios_de(text)                   to anon, authenticated;

-- ---------------------------------------------------------------------
-- RESUMO PARA VOCÊ: todos os números por certificação, num só lugar.
-- Veja em SQL Editor:  select * from resumo;
-- (ou Table Editor > resumo). Não fica disponível para o site.
-- ---------------------------------------------------------------------
create or replace view public.resumo as
with c as (
  select cert from curtidas union select cert from metas
  union select cert from compartilhamentos union select cert from comentarios
)
select c.cert as certificacao,
  (select count(*) from curtidas x where x.cert = c.cert)                                as curtidas,
  (select count(*) from metas x where x.cert = c.cert)                                   as salvos,
  (select count(*) from comentarios x where x.cert = c.cert and x.aprovado)              as comentarios,
  (select count(*) from comentarios x where x.cert = c.cert and not x.aprovado)          as pendentes,
  (select count(*) from compartilhamentos x where x.cert = c.cert and x.canal = 'linkedin') as linkedin,
  (select count(*) from compartilhamentos x where x.cert = c.cert and x.canal = 'whatsapp') as whatsapp,
  (select count(*) from compartilhamentos x where x.cert = c.cert and x.canal not in ('linkedin','whatsapp')) as outros_compart
from c
order by salvos desc, curtidas desc;
revoke all on public.resumo from anon, authenticated;
