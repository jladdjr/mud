--
-- PostgreSQL database dump
--

-- Dumped from database version 13.5 (Debian 13.5-0+deb11u1)
-- Dumped by pg_dump version 13.5 (Debian 13.5-0+deb11u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: file_metadata_snapshots; Type: TABLE; Schema: public; Owner: mud
--

CREATE TABLE public.file_metadata_snapshots (
    file_metadata_snapshot_id integer NOT NULL,
    machine_id integer,
    dir_path text,
    file_name text,
    scan_time timestamp without time zone,
    file_size integer,
    sha1 text,
    created timestamp without time zone,
    modified timestamp without time zone
);


ALTER TABLE public.file_metadata_snapshots OWNER TO mud;

--
-- Name: machines; Type: TABLE; Schema: public; Owner: mud
--

CREATE TABLE public.machines (
    machine_id integer NOT NULL,
    hostname text,
    description text
);


ALTER TABLE public.machines OWNER TO mud;

--
-- Name: scan_sessions; Type: TABLE; Schema: public; Owner: mud
--

CREATE TABLE public.scan_sessions (
    scan_session_id integer NOT NULL,
    scan_state_id integer,
    scan_start timestamp without time zone,
    scan_stop timestamp without time zone,
    scanned_machine_id integer
);


ALTER TABLE public.scan_sessions OWNER TO mud;

--
-- Name: scan_states; Type: TABLE; Schema: public; Owner: mud
--

CREATE TABLE public.scan_states (
    scan_state_id integer NOT NULL,
    scan_state text
);


ALTER TABLE public.scan_states OWNER TO mud;

--
-- Data for Name: file_metadata_snapshots; Type: TABLE DATA; Schema: public; Owner: mud
--

COPY public.file_metadata_snapshots (file_metadata_snapshot_id, machine_id, dir_path, file_name, scan_time, file_size, sha1, created, modified) FROM stdin;
\.


--
-- Data for Name: machines; Type: TABLE DATA; Schema: public; Owner: mud
--

COPY public.machines (machine_id, hostname, description) FROM stdin;
\.


--
-- Data for Name: scan_sessions; Type: TABLE DATA; Schema: public; Owner: mud
--

COPY public.scan_sessions (scan_session_id, scan_state_id, scan_start, scan_stop, scanned_machine_id) FROM stdin;
\.


--
-- Data for Name: scan_states; Type: TABLE DATA; Schema: public; Owner: mud
--

COPY public.scan_states (scan_state_id, scan_state) FROM stdin;
\.


--
-- Name: file_metadata_snapshots file_metadata_snapshots_pkey; Type: CONSTRAINT; Schema: public; Owner: mud
--

ALTER TABLE ONLY public.file_metadata_snapshots
    ADD CONSTRAINT file_metadata_snapshots_pkey PRIMARY KEY (file_metadata_snapshot_id);


--
-- Name: machines machines_pkey; Type: CONSTRAINT; Schema: public; Owner: mud
--

ALTER TABLE ONLY public.machines
    ADD CONSTRAINT machines_pkey PRIMARY KEY (machine_id);


--
-- Name: scan_sessions scan_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: mud
--

ALTER TABLE ONLY public.scan_sessions
    ADD CONSTRAINT scan_sessions_pkey PRIMARY KEY (scan_session_id);


--
-- Name: scan_states scan_states_pkey; Type: CONSTRAINT; Schema: public; Owner: mud
--

ALTER TABLE ONLY public.scan_states
    ADD CONSTRAINT scan_states_pkey PRIMARY KEY (scan_state_id);


--
-- Name: scan_sessions machines_fk; Type: FK CONSTRAINT; Schema: public; Owner: mud
--

ALTER TABLE ONLY public.scan_sessions
    ADD CONSTRAINT machines_fk FOREIGN KEY (scanned_machine_id) REFERENCES public.machines(machine_id);


--
-- Name: file_metadata_snapshots machines_fk; Type: FK CONSTRAINT; Schema: public; Owner: mud
--

ALTER TABLE ONLY public.file_metadata_snapshots
    ADD CONSTRAINT machines_fk FOREIGN KEY (machine_id) REFERENCES public.machines(machine_id);


--
-- Name: scan_sessions scan_states_fk; Type: FK CONSTRAINT; Schema: public; Owner: mud
--

ALTER TABLE ONLY public.scan_sessions
    ADD CONSTRAINT scan_states_fk FOREIGN KEY (scan_state_id) REFERENCES public.scan_states(scan_state_id);


--
-- PostgreSQL database dump complete
--

