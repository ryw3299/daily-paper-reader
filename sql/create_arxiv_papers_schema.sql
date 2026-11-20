-- arXiv 公共元数据表；字段与现有抓取、sync.py 和检索 RPC 保持一致。
-- 可重复执行，不删除已有论文。新 Supabase 实例需要先执行本文件，
-- 再执行 match_arxiv_papers.sql。

create extension if not exists vector;
set search_path = public, extensions;

create table if not exists public.arxiv_papers (
  id text primary key,
  source text not null default 'arxiv',
  source_paper_id text,
  doi text,
  version text,
  title text not null,
  abstract text,
  authors jsonb not null default '[]'::jsonb,
  primary_category text,
  categories jsonb not null default '[]'::jsonb,
  published timestamptz,
  link text,
  pdf_url text,
  embedding vector(384),
  embedding_model text,
  embedding_dim int,
  embedding_updated_at timestamptz,
  updated_at timestamptz not null default now(),
  search_tsv tsvector generated always as (
    to_tsvector('english', coalesce(title, '') || ' ' || coalesce(abstract, ''))
  ) stored
);

create index if not exists arxiv_papers_source_published_idx
  on public.arxiv_papers (source, published desc);
create index if not exists arxiv_papers_published_idx
  on public.arxiv_papers (published desc);
create index if not exists idx_arxiv_papers_search_tsv
  on public.arxiv_papers using gin (search_tsv);

alter table public.arxiv_papers enable row level security;
grant usage on schema public to anon, authenticated, service_role;
grant select on public.arxiv_papers to anon, authenticated;
grant all on public.arxiv_papers to service_role;
drop policy if exists "public read arxiv papers" on public.arxiv_papers;
create policy "public read arxiv papers" on public.arxiv_papers
  for select to anon, authenticated using (source = 'arxiv');
