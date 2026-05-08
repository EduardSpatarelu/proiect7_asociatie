--
-- PostgreSQL database dump
--

\restrict jrzhJRjGzMmnVARnlr5nwpovUiTbkks0HRLhWfbild6epOP73VN9H2Jd4Rvj629

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

-- Started on 2026-05-06 17:18:47

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- TOC entry 221 (class 1259 OID 16885)
-- Name: administrators; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.administrators (
    user_id integer NOT NULL,
    numar_atestat character varying(100)
);


ALTER TABLE public.administrators OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16897)
-- Name: apartments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.apartments (
    id integer NOT NULL,
    room_count integer NOT NULL,
    resident_count integer DEFAULT 0 NOT NULL,
    CONSTRAINT apartments_resident_count_check CHECK ((resident_count >= 0)),
    CONSTRAINT apartments_room_count_check CHECK ((room_count > 0))
);


ALTER TABLE public.apartments OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16896)
-- Name: apartments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.apartments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.apartments_id_seq OWNER TO postgres;

--
-- TOC entry 5106 (class 0 OID 0)
-- Dependencies: 222
-- Name: apartments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.apartments_id_seq OWNED BY public.apartments.id;


--
-- TOC entry 234 (class 1259 OID 16988)
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    id integer NOT NULL,
    nume_complet character varying(150) NOT NULL,
    salariu_brut numeric(10,2) NOT NULL,
    CONSTRAINT employees_salariu_brut_check CHECK ((salariu_brut >= (0)::numeric))
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 16987)
-- Name: employees_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employees_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employees_id_seq OWNER TO postgres;

--
-- TOC entry 5107 (class 0 OID 0)
-- Dependencies: 233
-- Name: employees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employees_id_seq OWNED BY public.employees.id;


--
-- TOC entry 228 (class 1259 OID 16940)
-- Name: invoices; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invoices (
    id integer NOT NULL,
    amount numeric(10,2) NOT NULL,
    date date NOT NULL,
    supplier_id integer,
    CONSTRAINT invoices_amount_check CHECK ((amount >= (0)::numeric))
);


ALTER TABLE public.invoices OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16939)
-- Name: invoices_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.invoices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.invoices_id_seq OWNER TO postgres;

--
-- TOC entry 5108 (class 0 OID 0)
-- Dependencies: 227
-- Name: invoices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.invoices_id_seq OWNED BY public.invoices.id;


--
-- TOC entry 224 (class 1259 OID 16909)
-- Name: locatari; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.locatari (
    user_id integer NOT NULL,
    nume_complet character varying(150) NOT NULL,
    este_proprietar boolean DEFAULT false,
    apartament_id integer
);


ALTER TABLE public.locatari OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 16972)
-- Name: payments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payments (
    id integer NOT NULL,
    amount numeric(10,2) NOT NULL,
    date date NOT NULL,
    apartment_id integer,
    CONSTRAINT payments_amount_check CHECK ((amount > (0)::numeric))
);


ALTER TABLE public.payments OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16971)
-- Name: payments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.payments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payments_id_seq OWNER TO postgres;

--
-- TOC entry 5109 (class 0 OID 0)
-- Dependencies: 231
-- Name: payments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.payments_id_seq OWNED BY public.payments.id;


--
-- TOC entry 226 (class 1259 OID 16928)
-- Name: suppliers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.suppliers (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    fiscal_code character varying(50) NOT NULL
);


ALTER TABLE public.suppliers OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16927)
-- Name: suppliers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.suppliers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.suppliers_id_seq OWNER TO postgres;

--
-- TOC entry 5110 (class 0 OID 0)
-- Dependencies: 225
-- Name: suppliers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.suppliers_id_seq OWNED BY public.suppliers.id;


--
-- TOC entry 220 (class 1259 OID 16872)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(100) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role character varying(50) NOT NULL,
    CONSTRAINT users_role_check CHECK (((role)::text = ANY ((ARRAY['Administrator'::character varying, 'User'::character varying])::text[])))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16871)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 5111 (class 0 OID 0)
-- Dependencies: 219
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 230 (class 1259 OID 16956)
-- Name: waterconsumption; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.waterconsumption (
    id integer NOT NULL,
    index_value integer NOT NULL,
    date date NOT NULL,
    apartament_id integer,
    CONSTRAINT waterconsumption_index_value_check CHECK ((index_value >= 0))
);


ALTER TABLE public.waterconsumption OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16955)
-- Name: waterconsumption_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.waterconsumption_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.waterconsumption_id_seq OWNER TO postgres;

--
-- TOC entry 5112 (class 0 OID 0)
-- Dependencies: 229
-- Name: waterconsumption_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.waterconsumption_id_seq OWNED BY public.waterconsumption.id;


--
-- TOC entry 4895 (class 2604 OID 16900)
-- Name: apartments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.apartments ALTER COLUMN id SET DEFAULT nextval('public.apartments_id_seq'::regclass);


--
-- TOC entry 4902 (class 2604 OID 16991)
-- Name: employees id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees ALTER COLUMN id SET DEFAULT nextval('public.employees_id_seq'::regclass);


--
-- TOC entry 4899 (class 2604 OID 16943)
-- Name: invoices id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices ALTER COLUMN id SET DEFAULT nextval('public.invoices_id_seq'::regclass);


--
-- TOC entry 4901 (class 2604 OID 16975)
-- Name: payments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments ALTER COLUMN id SET DEFAULT nextval('public.payments_id_seq'::regclass);


--
-- TOC entry 4898 (class 2604 OID 16931)
-- Name: suppliers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.suppliers ALTER COLUMN id SET DEFAULT nextval('public.suppliers_id_seq'::regclass);


--
-- TOC entry 4894 (class 2604 OID 16875)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4900 (class 2604 OID 16959)
-- Name: waterconsumption id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.waterconsumption ALTER COLUMN id SET DEFAULT nextval('public.waterconsumption_id_seq'::regclass);


--
-- TOC entry 5087 (class 0 OID 16885)
-- Dependencies: 221
-- Data for Name: administrators; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.administrators (user_id, numar_atestat) FROM stdin;
1	AT-123456
\.


--
-- TOC entry 5089 (class 0 OID 16897)
-- Dependencies: 223
-- Data for Name: apartments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.apartments (id, room_count, resident_count) FROM stdin;
1	2	2
2	3	4
3	1	1
\.


--
-- TOC entry 5100 (class 0 OID 16988)
-- Dependencies: 234
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employees (id, nume_complet, salariu_brut) FROM stdin;
1	Ionescu Maria (Femeie de serviciu)	1500.00
2	Georgescu Vasile (Administrator)	2000.00
\.


--
-- TOC entry 5094 (class 0 OID 16940)
-- Dependencies: 228
-- Data for Name: invoices; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invoices (id, amount, date, supplier_id) FROM stdin;
1	450.50	2026-05-01	1
2	200.00	2026-05-03	2
3	150.00	2026-05-05	3
\.


--
-- TOC entry 5090 (class 0 OID 16909)
-- Dependencies: 224
-- Data for Name: locatari; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.locatari (user_id, nume_complet, este_proprietar, apartament_id) FROM stdin;
2	Popescu Ion	t	1
\.


--
-- TOC entry 5098 (class 0 OID 16972)
-- Dependencies: 232
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payments (id, amount, date, apartment_id) FROM stdin;
1	100.00	2026-05-06	1
\.


--
-- TOC entry 5092 (class 0 OID 16928)
-- Dependencies: 226
-- Data for Name: suppliers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.suppliers (id, name, fiscal_code) FROM stdin;
1	Compania de Apa Oltenia	RO123456
2	CEZ Vanzare	RO987654
3	Salubritate Craiova	RO112233
\.


--
-- TOC entry 5086 (class 0 OID 16872)
-- Dependencies: 220
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password_hash, role) FROM stdin;
1	admin_asociatie	parola_admin123	Administrator
2	user_etaj1	parola_user123	User
\.


--
-- TOC entry 5096 (class 0 OID 16956)
-- Dependencies: 230
-- Data for Name: waterconsumption; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.waterconsumption (id, index_value, date, apartament_id) FROM stdin;
1	120	2026-05-04	1
2	340	2026-05-04	2
3	55	2026-05-04	3
\.


--
-- TOC entry 5113 (class 0 OID 0)
-- Dependencies: 222
-- Name: apartments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.apartments_id_seq', 3, true);


--
-- TOC entry 5114 (class 0 OID 0)
-- Dependencies: 233
-- Name: employees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employees_id_seq', 2, true);


--
-- TOC entry 5115 (class 0 OID 0)
-- Dependencies: 227
-- Name: invoices_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.invoices_id_seq', 3, true);


--
-- TOC entry 5116 (class 0 OID 0)
-- Dependencies: 231
-- Name: payments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.payments_id_seq', 1, true);


--
-- TOC entry 5117 (class 0 OID 0)
-- Dependencies: 225
-- Name: suppliers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.suppliers_id_seq', 3, true);


--
-- TOC entry 5118 (class 0 OID 0)
-- Dependencies: 219
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- TOC entry 5119 (class 0 OID 0)
-- Dependencies: 229
-- Name: waterconsumption_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.waterconsumption_id_seq', 3, true);


--
-- TOC entry 4915 (class 2606 OID 16890)
-- Name: administrators administrators_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administrators
    ADD CONSTRAINT administrators_pkey PRIMARY KEY (user_id);


--
-- TOC entry 4917 (class 2606 OID 16908)
-- Name: apartments apartments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.apartments
    ADD CONSTRAINT apartments_pkey PRIMARY KEY (id);


--
-- TOC entry 4931 (class 2606 OID 16997)
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- TOC entry 4925 (class 2606 OID 16949)
-- Name: invoices invoices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_pkey PRIMARY KEY (id);


--
-- TOC entry 4919 (class 2606 OID 16916)
-- Name: locatari locatari_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locatari
    ADD CONSTRAINT locatari_pkey PRIMARY KEY (user_id);


--
-- TOC entry 4929 (class 2606 OID 16981)
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- TOC entry 4921 (class 2606 OID 16938)
-- Name: suppliers suppliers_fiscal_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_fiscal_code_key UNIQUE (fiscal_code);


--
-- TOC entry 4923 (class 2606 OID 16936)
-- Name: suppliers suppliers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_pkey PRIMARY KEY (id);


--
-- TOC entry 4911 (class 2606 OID 16882)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4913 (class 2606 OID 16884)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4927 (class 2606 OID 16965)
-- Name: waterconsumption waterconsumption_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.waterconsumption
    ADD CONSTRAINT waterconsumption_pkey PRIMARY KEY (id);


--
-- TOC entry 4932 (class 2606 OID 16891)
-- Name: administrators administrators_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administrators
    ADD CONSTRAINT administrators_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4935 (class 2606 OID 16950)
-- Name: invoices invoices_supplier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES public.suppliers(id) ON DELETE CASCADE;


--
-- TOC entry 4933 (class 2606 OID 16922)
-- Name: locatari locatari_apartament_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locatari
    ADD CONSTRAINT locatari_apartament_id_fkey FOREIGN KEY (apartament_id) REFERENCES public.apartments(id) ON DELETE SET NULL;


--
-- TOC entry 4934 (class 2606 OID 16917)
-- Name: locatari locatari_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locatari
    ADD CONSTRAINT locatari_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4937 (class 2606 OID 16982)
-- Name: payments payments_apartment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_apartment_id_fkey FOREIGN KEY (apartment_id) REFERENCES public.apartments(id) ON DELETE CASCADE;


--
-- TOC entry 4936 (class 2606 OID 16966)
-- Name: waterconsumption waterconsumption_apartament_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.waterconsumption
    ADD CONSTRAINT waterconsumption_apartament_id_fkey FOREIGN KEY (apartament_id) REFERENCES public.apartments(id) ON DELETE CASCADE;


-- Completed on 2026-05-06 17:18:47

--
-- PostgreSQL database dump complete
--

\unrestrict jrzhJRjGzMmnVARnlr5nwpovUiTbkks0HRLhWfbild6epOP73VN9H2Jd4Rvj629

