"""UI text in English (en) and Bahasa Melayu (ms). Data values and dataset IDs stay as published by DOSM."""

TEXT = {
    "en": {
        "filters": "Filters", "state": "State (drill-down)", "all_my": "All Malaysia", "dtype": "District type",
        "weights": "Index weights", "weights_cap": "Move a slider up for the problems that matter most to you. All at 1.00 = everything counts equally.",
        "levels": ["Not counted", "Less important", "Normal", "More important", "Most important"],
        "up_income": "The higher it is, the more districts with <b>low household income</b> move up the priority list.",
        "up_poverty": "The higher it is, the more districts with <b>many poor households</b> move up the list.",
        "up_unemp": "The higher it is, the more districts with <b>many people looking for work</b> move up the list.",
        "up_particip": "The higher it is, the more districts where <b>few adults are working or job-hunting</b> move up the list.",
        "w_income": "Low income", "w_poverty": "Poverty", "w_unemp": "Unemployment", "w_particip": "Low participation",
        "h_income": "Household income = how much a family earns in a month (median, 2022). Lower income means a bigger decent-work gap.",
        "h_poverty": "Poverty = share of households earning below the national poverty line (2022).",
        "h_unemp": "Unemployment = share of the workforce who have no job but are looking for one (2022).",
        "h_particip": "Participation = share of working-age adults (15–64) who are working or looking for work. Low participation was the strongest sign of low income in our model.",
        "pill_data": "Official OpenDOSM data", "pill_sdg": "SDG 8 · Decent work", "pill_n": "{n} districts · 2019–2024",
        "hero_q": "Does having a job mean having decent work?",
        "hero_p": "Low unemployment can hide low pay. MyWajarScope finds the Malaysian districts where work is not yet "
                  "decent, and shows where to act first.",
        "k1": "Districts analysed", "k1s": "Joined across 4 official datasets",
        "k2": "Low-income trap", "k2u": "districts", "k2s": "{n} of them in Sabah",
        "k3": "Income gap · hub vs trap", "k3s": "Median household income per month",
        "k4": "Unemployment gap", "k4s": "Working-poor rural vs hubs, yet ~40% lower income",
        "tabs": ["Map", "District types", "Priority list", "2019 → 2024", "Drivers & what-if", "About"],
        "modes": {"cluster": "District type", "dwgi": "Gap index", "inc_med_2022": "Income",
                  "pov_abs_2022": "Poverty", "u_rate": "Unemployment", "p_rate": "Participation"},
        "sel_area": "Selected area", "s_shown": "Districts shown", "s_inc": "Median household income",
        "s_pov": "Average absolute poverty", "s_gap": "Largest decent-work gap",
        "tip_gap": "Gap index", "tip_inc": "Median income", "tip_pov": "Poverty", "tip_u": "Unemployment",
        "tip_p": "Participation", "tip_none": "No district labour data",
        "types_t": "Four types of district",
        "types_s": "K-Means clustering on 8 standardised labour-market and economic features",
        "prof_cols": ["Districts", "Median income (RM)", "Poverty %", "Unemployment %", "Participation %",
                      "Agriculture % GDP", "Manufacturing % GDP"],
        "insight": "<b>Employed is not the same as decently employed.</b> Working-poor rural districts have "
                   "unemployment almost as low as industrial hubs, yet ~40% lower income and ~4× the poverty.",
        "sc1": "Employed but not well-paid", "sc2": "Participation tracks income",
        "mix_t": "District types by state", "n_districts": "Districts",
        "prio_t": "Where should decent-work programmes go first?",
        "prio_s": "Decent Work Gap Index (0–100): weighted mix of low income, poverty, unemployment and low "
                  "participation. Move the weights in the sidebar and the ranking updates live.",
        "topn": "Show top N districts",
        "pcols": {"Rank": "Rank", "state": "State", "district": "District", "cluster": "Type", "DWGI": "DWGI",
                  "inc": "Median income (RM)", "pov": "Poverty %", "u": "Unemp %", "p": "LFPR %", "agri": "Agri % GDP"},
        "dl_prio": "Download priority list (CSV)",
        "trend_t": "Is the gap closing? 2019 → 2024", "trend_s": "Median change within each district type (nominal RM)",
        "tr_inc": "Income growth", "tr_inc_y": "Median income growth (%)",
        "tr_pov": "Poverty change", "tr_pov_y": "Change in absolute poverty (pp)",
        "compare": "Compare districts", "paths": "Income path of selected districts",
        "paths_y": "Median household income (RM)",
        "trend_cap": "Very small districts can swing sharply between survey rounds; read single-district extremes with care.",
        "ai_t": "What drives district income?", "ai_s": "Random Forest, 5-fold cross-validated R² = {r2:.2f}",
        "imp_t": "Driver importance", "imp_x": "Permutation importance",
        "imp_cap": "Participation and economic structure explain income far better than the unemployment rate.",
        "sim_t": "What-if simulator",
        "sim_s": "Change a district's labour market or economic mix and see the model's estimate. "
                 "Illustrative: an association, not a causal forecast.",
        "sim_d": "District", "sim_now": "Model estimate now", "sim_new": "With changes",
        "sim_bars": ["Now", "With changes", "Industrial-hub median"], "sim_actual": "Actual 2022 median income: RM{v:,.0f}",
        "about_t": "Data & method", "dl_all": "Download full district dataset (CSV)",
        "about_md": """
**Official sources (OpenDOSM, Department of Statistics Malaysia)**
- Household Income by Administrative District (`hh_income_district`) — 2019, 2022, 2024
- Poverty by Administrative District (`hh_poverty_district`) — 2019, 2022, 2024
- Annual Principal Labour Force Statistics by District (`lfs_district`) — 2018–2024
- GDP by District & Economic Sector, constant 2015 prices (`gdp_district_real_supply`) — 2015–2020
- District boundaries: DOSM `administrative_2_district` GeoJSON

**Method**
1. Clean & harmonise district names across datasets (19 fixes) and join on state + district.
2. Build 8 features for 2022 (district GDP structure uses 2020, the latest published).
3. K-Means (k = 4, standardised features) → four district types.
4. Random Forest (5-fold CV) + permutation importance → drivers of income.
5. Decent Work Gap Index → transparent, adjustable priority ranking.

**Limitations:** district GDP ends 2020; W.P. Kuala Lumpur, Putrajaya, Labuan and Perlis lack district
labour-force data and are excluded; incomes are nominal; model results are associations, not causal effects.

**SDG alignment:** SDG 8.5 (decent work and equal pay), 8.6 (participation / NEET), 8.2 (productivity &
diversification).
""",
        "clusters": {"Industrial hub": "Industrial hub", "Mid-tier town": "Mid-tier town",
                     "Working-poor rural": "Working-poor rural", "Low-income trap": "Low-income trap"},
        "labels": {"u_rate": "Unemployment rate (%)", "p_rate": "Labour-force participation (%)",
                   "agri_share": "Agriculture share of GDP (%)", "mining_share": "Mining share (%)",
                   "mfg_share": "Manufacturing share (%)", "constr_share": "Construction share (%)",
                   "services_share": "Services share (%)", "log_gdp_per_worker": "GDP per worker (log)",
                   "inc_med_2022": "Median household income 2022 (RM)", "pov_abs_2022": "Absolute poverty 2022 (%)",
                   "dwgi": "Decent Work Gap Index (0–100)", "inc_growth_pct": "Income growth 2019→2024 (%)",
                   "state": "State", "cluster": "Type"},
    },
    "ms": {
        "filters": "Penapis", "state": "Negeri (fokus)", "all_my": "Seluruh Malaysia", "dtype": "Jenis daerah",
        "weights": "Pemberat indeks", "weights_cap": "Naikkan slider bagi masalah yang paling penting bagi anda. Semua pada 1.00 = semua sama penting.",
        "levels": ["Tidak dikira", "Kurang penting", "Biasa", "Lebih penting", "Paling penting"],
        "up_income": "Semakin naik, semakin tinggi kedudukan daerah yang <b>pendapatan isi rumahnya rendah</b> dalam senarai keutamaan.",
        "up_poverty": "Semakin naik, semakin tinggi kedudukan daerah yang <b>ramai isi rumah miskin</b>.",
        "up_unemp": "Semakin naik, semakin tinggi kedudukan daerah yang <b>ramai orang sedang mencari kerja</b>.",
        "up_particip": "Semakin naik, semakin tinggi kedudukan daerah yang <b>kurang orang dewasa bekerja atau mencari kerja</b>.",
        "w_income": "Pendapatan rendah", "w_poverty": "Kemiskinan", "w_unemp": "Pengangguran",
        "w_particip": "Penyertaan rendah",
        "h_income": "Pendapatan isi rumah = berapa banyak sesebuah keluarga peroleh sebulan (penengah, 2022). Pendapatan lebih rendah bermakna jurang kerja layak lebih besar.",
        "h_poverty": "Kemiskinan = peratus isi rumah yang berpendapatan di bawah garis kemiskinan negara (2022).",
        "h_unemp": "Pengangguran = peratus tenaga buruh yang tiada kerja tetapi sedang mencari kerja (2022).",
        "h_particip": "Penyertaan = peratus orang dewasa umur bekerja (15–64) yang bekerja atau sedang mencari kerja. Penyertaan rendah ialah petanda paling kuat pendapatan rendah dalam model kami.",
        "pill_data": "Data rasmi OpenDOSM", "pill_sdg": "SDG 8 · Kerja layak", "pill_n": "{n} daerah · 2019–2024",
        "hero_q": "Adakah mempunyai pekerjaan bermakna mempunyai kerja yang layak?",
        "hero_p": "Kadar pengangguran yang rendah boleh menyembunyikan gaji yang rendah. MyWajarScope mengenal pasti "
                  "daerah di Malaysia yang pekerjaannya belum layak, dan menunjukkan di mana perlu bertindak dahulu.",
        "k1": "Daerah dianalisis", "k1s": "Digabung daripada 4 set data rasmi",
        "k2": "Perangkap pendapatan rendah", "k2u": "daerah", "k2s": "{n} daripadanya di Sabah",
        "k3": "Jurang pendapatan · hab vs perangkap", "k3s": "Pendapatan isi rumah penengah sebulan",
        "k4": "Jurang pengangguran", "k4s": "Luar bandar miskin bekerja vs hab, namun pendapatan ~40% lebih rendah",
        "tabs": ["Peta", "Jenis daerah", "Senarai keutamaan", "2019 → 2024", "Pemacu & simulasi", "Maklumat"],
        "modes": {"cluster": "Jenis daerah", "dwgi": "Indeks jurang", "inc_med_2022": "Pendapatan",
                  "pov_abs_2022": "Kemiskinan", "u_rate": "Pengangguran", "p_rate": "Penyertaan"},
        "sel_area": "Kawasan dipilih", "s_shown": "Daerah dipaparkan", "s_inc": "Pendapatan isi rumah penengah",
        "s_pov": "Purata kemiskinan mutlak", "s_gap": "Jurang kerja layak terbesar",
        "tip_gap": "Indeks jurang", "tip_inc": "Pendapatan penengah", "tip_pov": "Kemiskinan",
        "tip_u": "Pengangguran", "tip_p": "Penyertaan", "tip_none": "Tiada data tenaga buruh daerah",
        "types_t": "Empat jenis daerah",
        "types_s": "Pengelompokan K-Means ke atas 8 ciri pasaran buruh dan ekonomi yang dipiawaikan",
        "prof_cols": ["Daerah", "Pendapatan penengah (RM)", "Kemiskinan %", "Pengangguran %", "Penyertaan %",
                      "Pertanian % KDNK", "Pembuatan % KDNK"],
        "insight": "<b>Bekerja tidak sama dengan bekerja secara layak.</b> Daerah luar bandar miskin bekerja mempunyai "
                   "kadar pengangguran hampir serendah hab perindustrian, namun pendapatan ~40% lebih rendah dan "
                   "kemiskinan ~4 kali ganda.",
        "sc1": "Bekerja tetapi bergaji rendah", "sc2": "Penyertaan seiring pendapatan",
        "mix_t": "Jenis daerah mengikut negeri", "n_districts": "Daerah",
        "prio_t": "Di mana program kerja layak perlu dilaksanakan dahulu?",
        "prio_s": "Indeks Jurang Kerja Layak (0–100): gabungan berpemberat pendapatan rendah, kemiskinan, "
                  "pengangguran dan penyertaan rendah. Gerakkan pemberat di sisi dan kedudukan dikemas kini serta-merta.",
        "topn": "Papar N daerah teratas",
        "pcols": {"Rank": "Kedudukan", "state": "Negeri", "district": "Daerah", "cluster": "Jenis", "DWGI": "DWGI",
                  "inc": "Pendapatan penengah (RM)", "pov": "Kemiskinan %", "u": "Pengangguran %", "p": "KPTB %",
                  "agri": "Pertanian % KDNK"},
        "dl_prio": "Muat turun senarai keutamaan (CSV)",
        "trend_t": "Adakah jurang semakin rapat? 2019 → 2024",
        "trend_s": "Perubahan penengah dalam setiap jenis daerah (RM nominal)",
        "tr_inc": "Pertumbuhan pendapatan", "tr_inc_y": "Pertumbuhan pendapatan penengah (%)",
        "tr_pov": "Perubahan kemiskinan", "tr_pov_y": "Perubahan kemiskinan mutlak (mata peratus)",
        "compare": "Bandingkan daerah", "paths": "Trajektori pendapatan daerah dipilih",
        "paths_y": "Pendapatan isi rumah penengah (RM)",
        "trend_cap": "Daerah yang sangat kecil boleh berubah mendadak antara pusingan survei; baca nilai ekstrem "
                     "satu daerah dengan berhati-hati.",
        "ai_t": "Apakah pemacu pendapatan daerah?",
        "ai_s": "Random Forest, R² pengesahan silang 5 lipatan = {r2:.2f}",
        "imp_t": "Kepentingan pemacu", "imp_x": "Kepentingan permutasi",
        "imp_cap": "Penyertaan dan struktur ekonomi menerangkan pendapatan jauh lebih baik daripada kadar pengangguran.",
        "sim_t": "Simulasi bagaimana-jika",
        "sim_s": "Ubah pasaran buruh atau campuran ekonomi sesebuah daerah dan lihat anggaran model. "
                 "Ilustrasi sahaja: perkaitan, bukan ramalan sebab-akibat.",
        "sim_d": "Daerah", "sim_now": "Anggaran model sekarang", "sim_new": "Selepas perubahan",
        "sim_bars": ["Sekarang", "Selepas perubahan", "Penengah hab perindustrian"],
        "sim_actual": "Pendapatan penengah sebenar 2022: RM{v:,.0f}",
        "about_t": "Data & kaedah", "dl_all": "Muat turun set data penuh daerah (CSV)",
        "about_md": """
**Sumber rasmi (OpenDOSM, Jabatan Perangkaan Malaysia)**
- Pendapatan Isi Rumah mengikut Daerah Pentadbiran (`hh_income_district`) — 2019, 2022, 2024
- Kemiskinan mengikut Daerah Pentadbiran (`hh_poverty_district`) — 2019, 2022, 2024
- Statistik Utama Tenaga Buruh Tahunan mengikut Daerah (`lfs_district`) — 2018–2024
- KDNK mengikut Daerah & Sektor Ekonomi, harga malar 2015 (`gdp_district_real_supply`) — 2015–2020
- Sempadan daerah: GeoJSON DOSM `administrative_2_district`

**Kaedah**
1. Membersih & menyelaraskan nama daerah merentas set data (19 pembetulan) dan gabung mengikut negeri + daerah.
2. Membina 8 ciri bagi 2022 (struktur KDNK daerah guna 2020, data terkini yang diterbitkan).
3. K-Means (k = 4, ciri dipiawaikan) → empat jenis daerah.
4. Random Forest (pengesahan silang 5 lipatan) + kepentingan permutasi → pemacu pendapatan.
5. Indeks Jurang Kerja Layak → kedudukan keutamaan yang telus dan boleh dilaras.

**Had kajian:** KDNK daerah berakhir 2020; W.P. Kuala Lumpur, Putrajaya, Labuan dan Perlis tiada data tenaga
buruh peringkat daerah dan dikecualikan; pendapatan adalah nominal; keputusan model ialah perkaitan, bukan kesan
sebab-akibat.

**Penjajaran SDG:** SDG 8.5 (kerja layak dan gaji saksama), 8.6 (penyertaan / NEET), 8.2 (produktiviti &
kepelbagaian).
""",
        "clusters": {"Industrial hub": "Hab perindustrian", "Mid-tier town": "Bandar pertengahan",
                     "Working-poor rural": "Luar bandar miskin bekerja", "Low-income trap": "Perangkap pendapatan rendah"},
        "labels": {"u_rate": "Kadar pengangguran (%)", "p_rate": "Kadar penyertaan tenaga buruh (%)",
                   "agri_share": "Bahagian pertanian dalam KDNK (%)", "mining_share": "Bahagian perlombongan (%)",
                   "mfg_share": "Bahagian pembuatan (%)", "constr_share": "Bahagian pembinaan (%)",
                   "services_share": "Bahagian perkhidmatan (%)", "log_gdp_per_worker": "KDNK per pekerja (log)",
                   "inc_med_2022": "Pendapatan isi rumah penengah 2022 (RM)",
                   "pov_abs_2022": "Kemiskinan mutlak 2022 (%)",
                   "dwgi": "Indeks Jurang Kerja Layak (0–100)", "inc_growth_pct": "Pertumbuhan pendapatan 2019→2024 (%)",
                   "state": "Negeri", "cluster": "Jenis"},
    },
}

# ---------- infographic (About / Maklumat tab) ----------
TEXT["en"]["info"] = {
    "h_k": "About the system",
    "h_p": "A district-level lens on SDG 8. It joins four official OpenDOSM datasets to show where Malaysians "
           "are working but not yet earning a decent living, and where programmes should go first.",
    "st": ["districts analysed", "district names harmonised", "features per district", "district types found",
           "cross-validated R² (income model)"],
    "s1_t": "Four official datasets, one district view",
    "s1_p": "Every number comes from the Department of Statistics Malaysia. The bars show which years each dataset covers.",
    "src": {"income": ("Household income", "Median & mean, by district"),
            "poverty": ("Poverty", "Absolute & relative, by district"),
            "labour": ("Labour force", "Unemployment & participation"),
            "gdp": ("District GDP", "By sector, constant 2015 prices")},
    "s2_t": "From raw tables to a priority list",
    "s2_p": "Five steps, all reproducible in the project notebook.",
    "steps": [("Clean & harmonise", "District names are spelled differently across datasets and years "
               "(e.g. S.P.Tengah vs Seberang Perai Tengah). 19 fixes make the join lossless.", "Data quality"),
              ("Join & engineer features", "Income, poverty, unemployment, participation, sector shares and GDP per "
               "worker are combined into one row per district (2022).", "8 features"),
              ("Cluster districts", "K-Means groups districts with similar labour-market and economic profiles.",
               "K-Means · k = 4"),
              ("Explain income", "A Random Forest with permutation importance shows which factors move district "
               "income the most.", "Random Forest · 5-fold CV"),
              ("Rank where to act", "The Decent Work Gap Index combines low income, poverty, unemployment and low "
               "participation into a transparent 0–100 score with adjustable weights.", "DWGI 0–100")],
    "s3_t": "Four types of district",
    "s3_p": "Bars compare each type's median household income, absolute poverty and unemployment rate.",
    "districts": "districts", "m_inc": "Median income", "m_pov": "Poverty", "m_u": "Unemployment",
    "f_k": "Key finding", "f_t": "Having a job is not the same as having decent work",
    "f_u": "Unemployment", "f_un": "Almost the same…", "f_i": "Median household income", "f_in": "…but very different pay",
    "f_v": "<b>Working-poor rural districts look healthy on unemployment, yet earn far less and carry ~4× the poverty.</b> "
           "Participation and economic structure explain district income far better than the unemployment rate.",
    "s4_t": "Aligned with SDG 8",
    "sdg": [("8.5", "Decent work & equal pay", "Find districts where people work but pay stays low."),
            ("8.6", "Participation & NEET", "Low labour-force participation is the strongest income driver."),
            ("8.2", "Productivity & diversification", "Agriculture-heavy economies trail; diversification matters.")],
    "s5_t": "Limitations, stated openly",
    "lim": ["District GDP is published only up to 2020, so economic structure uses 2020.",
            "W.P. Kuala Lumpur, Putrajaya, Labuan and Perlis have no district labour-force data and are excluded.",
            "Incomes are nominal (not inflation-adjusted); very small districts can swing between survey rounds.",
            "Model results are statistical associations, not causal effects; the what-if simulator is illustrative."],
}
TEXT["ms"]["info"] = {
    "h_k": "Tentang sistem",
    "h_p": "Lensa peringkat daerah untuk SDG 8. Sistem ini menggabungkan empat set data rasmi OpenDOSM untuk "
           "menunjukkan di mana rakyat Malaysia bekerja tetapi belum memperoleh pendapatan yang layak, dan di mana "
           "program perlu dilaksanakan dahulu.",
    "st": ["daerah dianalisis", "nama daerah diselaraskan", "ciri bagi setiap daerah", "jenis daerah ditemui",
           "R² pengesahan silang (model pendapatan)"],
    "s1_t": "Empat set data rasmi, satu paparan daerah",
    "s1_p": "Setiap angka datang daripada Jabatan Perangkaan Malaysia. Bar menunjukkan tahun yang diliputi setiap set data.",
    "src": {"income": ("Pendapatan isi rumah", "Penengah & purata, mengikut daerah"),
            "poverty": ("Kemiskinan", "Mutlak & relatif, mengikut daerah"),
            "labour": ("Tenaga buruh", "Pengangguran & penyertaan"),
            "gdp": ("KDNK daerah", "Mengikut sektor, harga malar 2015")},
    "s2_t": "Daripada jadual mentah kepada senarai keutamaan",
    "s2_p": "Lima langkah, semuanya boleh diulang dalam notebook projek.",
    "steps": [("Bersih & selaras", "Nama daerah dieja berbeza merentas set data dan tahun "
               "(cth. S.P.Tengah vs Seberang Perai Tengah). 19 pembetulan memastikan tiada data tercicir.", "Kualiti data"),
              ("Gabung & bina ciri", "Pendapatan, kemiskinan, pengangguran, penyertaan, bahagian sektor dan KDNK per "
               "pekerja digabung menjadi satu baris bagi setiap daerah (2022).", "8 ciri"),
              ("Kelompokkan daerah", "K-Means mengumpulkan daerah yang mempunyai profil pasaran buruh dan ekonomi serupa.",
               "K-Means · k = 4"),
              ("Terangkan pendapatan", "Random Forest dengan kepentingan permutasi menunjukkan faktor yang paling "
               "mempengaruhi pendapatan daerah.", "Random Forest · CV 5 lipatan"),
              ("Susun keutamaan", "Indeks Jurang Kerja Layak menggabungkan pendapatan rendah, kemiskinan, pengangguran "
               "dan penyertaan rendah menjadi skor 0–100 yang telus dengan pemberat boleh dilaras.", "DWGI 0–100")],
    "s3_t": "Empat jenis daerah",
    "s3_p": "Bar membandingkan pendapatan isi rumah penengah, kemiskinan mutlak dan kadar pengangguran setiap jenis.",
    "districts": "daerah", "m_inc": "Pendapatan penengah", "m_pov": "Kemiskinan", "m_u": "Pengangguran",
    "f_k": "Dapatan utama", "f_t": "Mempunyai pekerjaan tidak sama dengan mempunyai kerja yang layak",
    "f_u": "Pengangguran", "f_un": "Hampir sama…", "f_i": "Pendapatan isi rumah penengah", "f_in": "…tetapi gaji jauh berbeza",
    "f_v": "<b>Daerah luar bandar miskin bekerja kelihatan baik dari segi pengangguran, namun berpendapatan jauh lebih "
           "rendah dan kemiskinan ~4 kali ganda.</b> Penyertaan dan struktur ekonomi menerangkan pendapatan daerah jauh "
           "lebih baik daripada kadar pengangguran.",
    "s4_t": "Selari dengan SDG 8",
    "sdg": [("8.5", "Kerja layak & gaji saksama", "Kenal pasti daerah yang rakyatnya bekerja tetapi gaji kekal rendah."),
            ("8.6", "Penyertaan & NEET", "Kadar penyertaan tenaga buruh yang rendah ialah pemacu pendapatan terkuat."),
            ("8.2", "Produktiviti & kepelbagaian", "Ekonomi berat pertanian ketinggalan; kepelbagaian penting.")],
    "s5_t": "Had kajian, dinyatakan secara terbuka",
    "lim": ["KDNK daerah hanya diterbitkan sehingga 2020, jadi struktur ekonomi menggunakan data 2020.",
            "W.P. Kuala Lumpur, Putrajaya, Labuan dan Perlis tiada data tenaga buruh peringkat daerah dan dikecualikan.",
            "Pendapatan adalah nominal (tidak dilaras inflasi); daerah yang sangat kecil boleh berubah antara pusingan survei.",
            "Keputusan model ialah perkaitan statistik, bukan kesan sebab-akibat; simulasi bagaimana-jika adalah ilustrasi."],
}

# ---------- final-submission features ----------
TEXT["en"].update({
    "tabs": ["Map", "District profile", "District types", "Priority list", "2019 → 2024", "Drivers & what-if", "About"],
    "all_zero": "All weights are 0, so equal weights are used instead.",
    "empty": "No districts match the current filters. Select at least one district type in the sidebar.",
    "method": {"dwgi": "Adjustable index (DWGI)", "topsis": "Data-driven (Entropy-TOPSIS)"},
    "method_note": {"dwgi": "Weights come from the sidebar sliders, so you can set the priorities.",
                    "topsis": "Weights come from the data itself (entropy): indicators that differ more between "
                              "districts count more. Nobody chooses the weights."},
    "agree_t": "Do both methods agree?",
    "agree_rho": "Rank correlation (Spearman)", "agree_top": "Shared districts in both top 20",
    "agree_w": "Data-driven weights",
    "w_names": {"inc_med_2022": "Income", "pov_abs_2022": "Poverty", "u_rate": "Unemployment", "p_rate": "Participation"},
    "score": "Gap score (0–100)",
    "prof_t": "District profile", "prof_s": "Everything about one district in one place, compared with the rest of Malaysia.",
    "pick": "Choose a district", "rank_of": "Rank {r} of {n}", "topsis_rank": "Entropy-TOPSIS rank {r}",
    "vs_nat": "vs Malaysia",
    "radar_t": "How it compares (percentile, 100 = best in Malaysia)",
    "radar_dims": ["Income", "Low poverty", "Low unemployment", "Participation", "Diversified economy", "Productivity"],
    "radar_series": ["This district", "Its district type", "Malaysia median"],
    "trend_mini": "Income and poverty, 2019 → 2024",
    "recs_t": "Suggested action areas", "recs_s": "Generated from this district's weakest indicators.",
    "recs": {
        "participation": ("Raise labour-force participation", "Childcare, flexible and home-based work, and outreach to "
                          "youth not in employment, education or training.", "SDG 8.5 · 8.6"),
        "jobs": ("Match people to jobs", "Local job-matching drives and short TVET upskilling tied to employers in the area.",
                 "SDG 8.5 · 8.6"),
        "agri": ("Move up the agri value chain", "Agro-processing, cooperatives and digital market access so farm work "
                 "pays more.", "SDG 8.2"),
        "poverty": ("Targeted income support", "Pair targeted assistance for poor households with livelihood "
                    "programmes so support leads to work.", "SDG 8.5 · 1.2"),
        "productivity": ("Lift productivity", "Basic infrastructure, connectivity and digital adoption for small firms.",
                         "SDG 8.2 · 9"),
        "falling": ("Watch: income fell since 2019", "Median household income is lower than in 2019; check for local "
                    "shocks before planning.", "Monitor"),
        "sustain": ("On track: sustain and share", "No indicator is far behind; document what works and share it with "
                    "similar districts.", "SDG 8"),
    },
    "peers_t": "Learn from similar districts",
    "peers_s": "Districts with the most similar economic structure that already have a smaller decent-work gap.",
    "peers_none": "No structurally similar district does better; this district is already among the best of its kind.",
    "dl_brief": "Download district brief (HTML, print to PDF)",
    "brief": {"title": "District brief", "rank": "Priority rank", "growth": "Median income growth 2019→2024",
              "actions": "Suggested action areas", "peers": "Similar districts doing better", "no_peers": "None found",
              "foot": "Source: OpenDOSM (DOSM) household income, poverty, labour force and district GDP. "
                      "Suggestions are rule-based starting points, not policy prescriptions."},
    "val_t": "Is the model reliable?", "val_x": "Actual (RM)", "val_y": "Predicted (RM)",
    "val_cap": "Each point is predicted by a model that never saw that district (5-fold cross-validation). Points near "
               "the diagonal = good predictions.",
    "foot": "MyWajarScope · MDIT 2026: Global Challenge · Data: OpenDOSM, Department of Statistics Malaysia "
            "(income & poverty 2019/2022/2024, labour force 2018–2024, district GDP 2015–2020).",
})
TEXT["ms"].update({
    "tabs": ["Peta", "Profil daerah", "Jenis daerah", "Senarai keutamaan", "2019 → 2024", "Pemacu & simulasi", "Maklumat"],
    "all_zero": "Semua pemberat 0, jadi pemberat sama digunakan.",
    "empty": "Tiada daerah sepadan dengan penapis semasa. Pilih sekurang-kurangnya satu jenis daerah di sisi.",
    "method": {"dwgi": "Indeks boleh laras (DWGI)", "topsis": "Berasaskan data (Entropy-TOPSIS)"},
    "method_note": {"dwgi": "Pemberat datang daripada slider di sisi, jadi anda boleh tetapkan keutamaan.",
                    "topsis": "Pemberat datang daripada data itu sendiri (entropi): penunjuk yang lebih berbeza antara "
                              "daerah diberi pemberat lebih. Tiada sesiapa memilih pemberat."},
    "agree_t": "Adakah kedua-dua kaedah sepakat?",
    "agree_rho": "Korelasi kedudukan (Spearman)", "agree_top": "Daerah yang sama dalam kedua-dua 20 teratas",
    "agree_w": "Pemberat berasaskan data",
    "w_names": {"inc_med_2022": "Pendapatan", "pov_abs_2022": "Kemiskinan", "u_rate": "Pengangguran",
                "p_rate": "Penyertaan"},
    "score": "Skor jurang (0–100)",
    "prof_t": "Profil daerah", "prof_s": "Semua maklumat satu daerah di satu tempat, dibandingkan dengan seluruh Malaysia.",
    "pick": "Pilih daerah", "rank_of": "Kedudukan {r} daripada {n}", "topsis_rank": "Kedudukan Entropy-TOPSIS {r}",
    "vs_nat": "vs Malaysia",
    "radar_t": "Perbandingan (persentil, 100 = terbaik di Malaysia)",
    "radar_dims": ["Pendapatan", "Kemiskinan rendah", "Pengangguran rendah", "Penyertaan", "Ekonomi pelbagai",
                   "Produktiviti"],
    "radar_series": ["Daerah ini", "Jenis daerahnya", "Penengah Malaysia"],
    "trend_mini": "Pendapatan dan kemiskinan, 2019 → 2024",
    "recs_t": "Cadangan bidang tindakan", "recs_s": "Dijana daripada penunjuk paling lemah daerah ini.",
    "recs": {
        "participation": ("Tingkatkan penyertaan tenaga buruh", "Penjagaan kanak-kanak, kerja fleksibel dan dari rumah, "
                          "serta jangkauan kepada belia yang tidak bekerja, belajar atau berlatih.", "SDG 8.5 · 8.6"),
        "jobs": ("Padankan rakyat dengan pekerjaan", "Program padanan kerja setempat dan latihan TVET jangka pendek "
                 "bersama majikan di kawasan itu.", "SDG 8.5 · 8.6"),
        "agri": ("Naikkan rantaian nilai pertanian", "Pemprosesan agro, koperasi dan akses pasaran digital supaya kerja "
                 "pertanian lebih berbaloi.", "SDG 8.2"),
        "poverty": ("Bantuan pendapatan bersasar", "Gandingkan bantuan bersasar untuk isi rumah miskin dengan program "
                    "sara hidup supaya bantuan membawa kepada pekerjaan.", "SDG 8.5 · 1.2"),
        "productivity": ("Tingkatkan produktiviti", "Infrastruktur asas, ketersambungan dan penggunaan digital untuk "
                         "perniagaan kecil.", "SDG 8.2 · 9"),
        "falling": ("Perhatian: pendapatan menurun sejak 2019", "Pendapatan isi rumah penengah lebih rendah berbanding "
                    "2019; semak kejutan setempat sebelum merancang.", "Pantau"),
        "sustain": ("Di landasan: kekalkan dan kongsi", "Tiada penunjuk yang jauh ketinggalan; dokumentasikan amalan "
                    "berkesan dan kongsi dengan daerah serupa.", "SDG 8"),
    },
    "peers_t": "Belajar daripada daerah serupa",
    "peers_s": "Daerah dengan struktur ekonomi paling serupa yang sudah mempunyai jurang kerja layak lebih kecil.",
    "peers_none": "Tiada daerah berstruktur serupa yang lebih baik; daerah ini sudah antara yang terbaik dalam jenisnya.",
    "dl_brief": "Muat turun ringkasan daerah (HTML, cetak ke PDF)",
    "brief": {"title": "Ringkasan daerah", "rank": "Kedudukan keutamaan",
              "growth": "Pertumbuhan pendapatan penengah 2019→2024", "actions": "Cadangan bidang tindakan",
              "peers": "Daerah serupa yang lebih baik", "no_peers": "Tiada",
              "foot": "Sumber: OpenDOSM (DOSM) pendapatan isi rumah, kemiskinan, tenaga buruh dan KDNK daerah. "
                      "Cadangan ialah titik permulaan berasaskan peraturan, bukan preskripsi dasar."},
    "val_t": "Adakah model boleh dipercayai?", "val_x": "Sebenar (RM)",
    "val_y": "Ramalan (RM)",
    "val_cap": "Setiap titik diramal oleh model yang tidak pernah melihat daerah itu (pengesahan silang 5 lipatan). "
               "Titik dekat garis pepenjuru = ramalan baik.",
    "foot": "MyWajarScope · MDIT 2026: Global Challenge · Data: OpenDOSM, Jabatan Perangkaan Malaysia "
            "(pendapatan & kemiskinan 2019/2022/2024, tenaga buruh 2018–2024, KDNK daerah 2015–2020).",
})
