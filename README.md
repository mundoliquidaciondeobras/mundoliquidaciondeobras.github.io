<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mundo Liquidación de Obras | Consultoría, Peritajes y Tasaciones</title>
    <!-- Fuente moderna Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --azul-principal: #0b3c5d;
            --azul-oscuro: #07253a;
            --naranja-acento: #f39c12;
            --blanco: #ffffff;
            --gris-claro: #f4f6f9;
            --texto: #333333;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            background-color: var(--gris-claro);
            color: var(--texto);
            line-height: 1.6;
        }

        /* Encabezado */
        header {
            background-color: var(--azul-principal);
            color: var(--blanco);
            padding: 1rem 5%;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .logo-img {
            height: 55px;
            width: auto;
            border-radius: 6px;
            object-fit: contain;
            background-color: var(--blanco);
            padding: 2px;
        }

        .logo h1 {
            font-size: 1.3rem;
            color: var(--blanco);
            font-weight: 700;
            line-height: 1.2;
        }

        .logo p {
            font-size: 0.75rem;
            color: var(--naranja-acento);
        }

        nav ul {
            display: flex;
            list-style: none;
            gap: 20px;
            align-items: center;
        }

        nav a {
            color: var(--blanco);
            text-decoration: none;
            font-weight: 500;
            font-size: 0.95rem;
            transition: 0.3s;
        }

        nav a:hover {
            color: var(--naranja-acento);
        }

        .nav-btn {
            background-color: var(--naranja-acento);
            color: var(--azul-oscuro) !important;
            padding: 8px 18px;
            border-radius: 20px;
            font-weight: 600;
        }

        .nav-btn:hover {
            background-color: #d68910;
        }

        /* Banner Principal (Hero) */
        .hero {
            background: linear-gradient(rgba(11, 60, 93, 0.88), rgba(7, 37, 58, 0.92)), 
                        url('https://images.unsplash.com/photo-1541888946425-d0fbb186a5b3?auto=format&fit=crop&w=1200&q=80') center/cover;
            color: var(--blanco);
            text-align: center;
            padding: 90px 20px;
        }

        .hero h2 {
            font-size: 2.2rem;
            margin-bottom: 15px;
            font-weight: 700;
        }

        .hero p {
            font-size: 1.05rem;
            max-width: 800px;
            margin: 0 auto 30px;
            opacity: 0.9;
        }

        .btn-cta {
            display: inline-block;
            background-color: var(--naranja-acento);
            color: var(--azul-oscuro);
            padding: 14px 32px;
            text-decoration: none;
            font-weight: bold;
            border-radius: 30px;
            transition: 0.3s;
            box-shadow: 0 4px 15px rgba(243, 156, 18, 0.4);
        }

        .btn-cta:hover {
            background-color: #e08e0b;
            transform: translateY(-2px);
        }

        /* Contenedores de Secciones */
        .section-padding {
            padding: 60px 20px;
        }

        .container {
            max-width: 1150px;
            margin: 0 auto;
        }

        .section-title {
            text-align: center;
            color: var(--azul-principal);
            margin-bottom: 10px;
            font-size: 1.9rem;
        }

        .section-subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 40px;
            font-size: 1rem;
        }

        /* Sección Nosotros */
        .nosotros-content {
            background: var(--blanco);
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            align-items: center;
        }

        .nosotros-text h3 {
            color: var(--azul-principal);
            margin-bottom: 15px;
            font-size: 1.4rem;
        }

        .nosotros-text p {
            color: #555;
            margin-bottom: 15px;
            font-size: 0.95rem;
        }

        /* Grilla de Servicios */
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
        }

        .card {
            background: var(--blanco);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            border-top: 5px solid var(--naranja-acento);
            transition: 0.3s;
            display: flex;
            flex-direction: column;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }

        .card h3 {
            color: var(--azul-principal);
            margin-bottom: 12px;
            font-size: 1.2rem;
        }

        .card p {
            color: #555;
            font-size: 0.92rem;
            line-height: 1.5;
        }

        /* Sección Biblioteca */
        .biblioteca-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }

        .doc-card {
            background: var(--blanco);
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid var(--azul-principal);
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }

        .doc-card h4 {
            color: var(--azul-oscuro);
            font-size: 1.05rem;
            margin-bottom: 8px;
        }

        .doc-card p {
            color: #666;
            font-size: 0.85rem;
            margin-bottom: 15px;
        }

        .btn-doc {
            display: inline-block;
            color: var(--naranja-acento);
            text-decoration: none;
            font-weight: 600;
            font-size: 0.85rem;
        }

        .btn-doc:hover {
            text-decoration: underline;
        }

        /* Bloque de Métricas */
        .features {
            background-color: var(--blanco);
            padding: 40px 20px;
            margin-top: 40px;
            border-radius: 10px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        }

        .feature-item h4 {
            color: var(--naranja-acento);
            font-size: 1.6rem;
            font-weight: 700;
        }

        .feature-item p {
            color: var(--azul-oscuro);
            font-weight: 600;
            font-size: 0.88rem;
        }

        /* Pie de página */
        footer {
            background-color: var(--azul-oscuro);
            color: var(--blanco);
            text-align: center;
            padding: 25px 20px;
            margin-top: 60px;
            font-size: 0.9rem;
        }

        /* Botón Flotante de WhatsApp */
        .btn-whatsapp {
            position: fixed;
            bottom: 25px;
            right: 25px;
            background-color: #25d366;
            color: white;
            border-radius: 50px;
            padding: 12px 22px;
            text-decoration: none;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(0,0,0,0.25);
            display: flex;
            align-items: center;
            gap: 8px;
            z-index: 1000;
        }

        .btn-whatsapp:hover {
            background-color: #128c7e;
        }

        @media (max-width: 768px) {
            header {
                flex-direction: column;
                gap: 15px;
            }
            nav ul {
                flex-wrap: wrap;
                justify-content: center;
            }
            .hero h2 {
                font-size: 1.6rem;
            }
        }
    </style>
</head>
<body>

    <!-- Header con Logotipo y Menú -->
    <header>
        <div class="logo">
            <img src="logo liqui.jpeg" alt="Mundo Liquidación de Obras" class="logo-img">
            <div>
                <h1>MUNDO LIQUIDACIÓN DE OBRAS</h1>
                <p>Conocimiento técnico que genera confianza</p>
            </div>
        </div>
        <nav>
            <ul>
                <li><a href="#inicio">Inicio</a></li>
                <li><a href="#nosotros">Nosotros</a></li>
                <li><a href="#servicios">Servicios</a></li>
                <li><a href="#biblioteca">Biblioteca</a></li>
                <li><a href="https://wa.me/51966630042" class="nav-btn" target="_blank">Contacto</a></li>
            </ul>
        </nav>
    </header>

    <!-- INICIO / HERO BANNER -->
    <section id="inicio" class="hero">
        <h2>Consultoría, Peritajes, Liquidación de Obras y Tasaciones Inmobiliarias</h2>
        <p>Asesoría técnica y legal especializada bajo la Ley N.° 32069, Ley N.° 30225 y reglamentos anteriores. Elaboración, revisión y sustentación pericial de expedientes en contratación pública y privada.</p>
        <a href="https://wa.me/51966630042?text=Hola,%20deseo%20consultar%20sobre%20un%20servicio" class="btn-cta" target="_blank">Consultar por WhatsApp</a>
    </section>

    <!-- NOSOTROS -->
    <section id="nosotros" class="section-padding container">
        <h2 class="section-title">Sobre Nosotros</h2>
        <p class="section-subtitle">Especialistas en ingeniería técnico-legal en obras públicas y privadas</p>
        
        <div class="nosotros-content">
            <div class="nosotros-text">
                <h3>Experiencia y Rigor Técnico al Servicio de sus Proyectos</h3>
                <p>En **Mundo Liquidación de Obras** brindamos servicios integrales de consultoría, peritajes, valorizaciones, reajustes, liquidaciones y tasaciones inmobiliarias en todo el Perú.</p>
                <p>Contamos con un dominio exhaustivo del marco normativo vigente (Ley N.° 32069) y marcos normativos históricos de Contrataciones del Estado (Ley N.° 30225 y sus reglamentos), asegurando soluciones sólidas ante entidades públicas, contratistas, JPRD y tribunales arbitrales.</p>
            </div>
            <div>
                <div class="doc-card" style="border-left-color: var(--naranja-acento);">
                    <h4>🎯 Misión</h4>
                    <p>Ofrecer soporte técnico-legal riguroso para la eficiente gestión de liquidaciones de contrato, resolución de controversias y valoración precisa de activos inmobiliarios.</p>
                </div>
                <div class="doc-card" style="border-left-color: var(--azul-principal); margin-top: 15px;">
                    <h4>👁️ Visión</h4>
                    <p>Ser la plataforma y firma consultora de referencia nacional en contratación pública, liquidación de obras y peritajes técnicos.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- SERVICIOS -->
    <section id="servicios" class="section-padding" style="background-color: #edf2f7;">
        <div class="container">
            <h2 class="section-title">Nuestros Servicios Especializados</h2>
            <p class="section-subtitle">Soluciones técnicas a la medida de contratistas y entidades del Estado</p>
            
            <div class="services-grid">
                <div class="card">
                    <h3>📜 Consultoría en Liquidación de Obras</h3>
                    <p>Elaboración y revisión técnico-financiera de expedientes de liquidación de contratos de obra pública y privada conforme a norma aplicable.</p>
                </div>
                <div class="card">
                    <h3>📊 Reajustes, GG y Penalidades</h3>
                    <p>Cálculo preciso de fórmulas polinómicas, reajustes K, cálculo de mayores gastos generales acreditados o variables, adicionales, deductivos, amortizaciones e intereses legales.</p>
                </div>
                <div class="card">
                    <h3>🏛️ Tasaciones Inmobiliarias</h3>
                    <p>Valuación comercial y reglamentaria de inmuebles, terrenos, infraestructura, expropiaciones, servidumbres e inventarios físicos de obras para entidades y privados.</p>
                </div>
                <div class="card">
                    <h3>⚖️ Peritajes Técnicos y Arbitraje</h3>
                    <p>Elaboración de informes periciales técnicos para controversias, Junta de Prevención y Resolución de Disputas (JPRD), conciliaciones y procesos arbitrales.</p>
                </div>
                <div class="card">
                    <h3>🎓 Capacitación y Asesoría Legal-Técnica</h3>
                    <p>Análisis comparativo y aplicación práctica de la Ley N.° 32069, Ley N.° 30225, reglamentos anteriores, opiniones del OECE y criterios jurisprudenciales.</p>
                </div>
            </div>

            <!-- Bloque de Métricas -->
            <div class="features">
                <div class="feature-item">
                    <h4>Marco Normativo</h4>
                    <p>Ley N.° 32069, N.° 30225 y reglamentos</p>
                </div>
                <div class="feature-item">
                    <h4>Tasaciones</h4>
                    <p>Valuación Comercial y Reglamentaria</p>
                </div>
                <div class="feature-item">
                    <h4>Peritajes</h4>
                    <p>Soporte en Controversias y Arbitrajes</p>
                </div>
            </div>
        </div>
    </section>

    <!-- BIBLIOTECA TÉCNICA -->
    <section id="biblioteca" class="section-padding container">
        <h2 class="section-title">Biblioteca Técnica</h2>
        <p class="section-subtitle">Documentos, normas y formatos de consulta frecuente</p>

        <div class="biblioteca-grid">
            <div class="doc-card">
                <h4>📜 Ley N.° 32069</h4>
                <p>Nueva Ley de Contrataciones del Estado y sus disposiciones clave para obras públicas.</p>
                <a href="https://wa.me/51966630042?text=Solicito%20información%20sobre%20Ley%2032069" class="btn-doc" target="_blank">Consultar Documento →</a>
            </div>
            <div class="doc-card">
                <h4>📘 Ley N.° 30225 y Reglamento</h4>
                <p>Compendio normativo anterior aplicable a contratos en ejecución y liquidación.</p>
                <a href="https://wa.me/51966630042?text=Solicito%20normativa%20Ley%2030225" class="btn-doc" target="_blank">Consultar Documento →</a>
            </div>
            <div class="doc-card">
                <h4>📊 Formatos de Liquidación</h4>
                <p>Modelos y hojas de cálculo para reajustes, fórmulas polinómicas y mayores gastos generales.</p>
                <a href="https://wa.me/51966630042?text=Solicito%20formatos%20de%20liquidación" class="btn-doc" target="_blank">Solicitar Formatos →</a>
            </div>
            <div class="doc-card">
                <h4>🏠 Reglamento Nacional de Tasaciones</h4>
                <p>Criterios técnicos oficiales para la valuación de predios urbanos y rústicos.</p>
                <a href="https://wa.me/51966630042?text=Solicito%20información%20de%20Tasaciones" class="btn-doc" target="_blank">Consultar Norma →</a>
            </div>
        </div>
    </section>

    <!-- Botón Flotante de WhatsApp -->
    <a href="https://wa.me/51966630042?text=Hola,%20deseo%20información%20sobre%20sus%20servicios" class="btn-whatsapp" target="_blank">
        💬 WhatsApp
    </a>

    <!-- Footer -->
    <footer>
        <p>© 2026 Mundo Liquidación de Obras. Correo: mundoliquidaciondeobras@gmail.com | WhatsApp: +51 966 630 042</p>
    </footer>

</body>
</html>
