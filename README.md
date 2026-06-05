PLAN DE MIGRACION
 El objetivo de este plan es detallar los pasos exactos para reescribir y migrar la aplicación actual "Barbería PANDA" de una arquitectura híbrida monolítica (Laravel/PHP) a una Arquitectura Desacoplada (Cliente-Servidor API-First) utilizando exclusivamente TypeScript, cumpliendo con las directrices académicas solicitadas.
El Frontend será construido con Angular, y el Backend con NestJS (el marco de trabajo más robusto para APIs en TypeScript, estructurado de manera muy similar a Angular).
WARNING
Esta migración implica reescribir toda la aplicación desde cero (Backend y Frontend). El código actual en Laravel (PHP) será descartado para la versión final y se generarán dos proyectos completamente independientes. 
Angular ➔ NestJS + Prisma ➔ Supabase
En este flujo, Supabase actúa únicamente como tu base de datos gestionada (PostgreSQL) en la nube y proveedor de infraestructura, mientras que NestJS expone la API pública.
¿Cómo funciona?: Angular consume endpoints REST o GraphQL expuestos exclusivamente por NestJS. Dentro de NestJS, utilizas el ORM Prisma para conectarte a la base de datos PostgreSQL que te proporciona Supabase.
Por qué es mejor para tu arquitectura:
Cumple con API-First: Tienes un contrato de API claro y centralizado en NestJS (usando Swagger/OpenAPI). Si mañana decides cambiar Supabase por AWS RDS o cualquier otra base de datos, tu frontend no se entera; solo cambias la conexión en Prisma.
Lógica de negocio segura: Toda las reglas complejas, validaciones y permisos se procesan en tu servidor backend (NestJS), sin exponer la estructura de tu base de datos al cliente.
Tipado de extremo a extremo: Prisma genera tipos de TypeScript automáticos basados en tu base de datos, que se integran perfectamente con NestJS y puedes compartir con Angular.
Estructura del Proyecto (Desacoplamiento Total)
Se separarán las responsabilidades en dos carpetas (repositorios) independientes:
sharkhub-backend/ (Lógica de negocio, validaciones y acceso a datos).
sharkhub-frontend/ (Interfaz de usuario, estilos y consumo de datos).
2. Frontend Cliente (Angular + TypeScript)
Toda la carpeta actual de /resources/views y /public de Laravel se transformará en un proyecto de Angular.
[NEW] Componentización de la Interfaz (UI)
El diseño actual (Black And White, botones Premium, HTML estructurado) se dividirá en Componentes reutilizables de Angular:
AppComponent: Contenedor principal con Navbar y Footer.
HomeComponent: Slider principal e información general.
ServicesComponent y PricingComponent: Vistas de servicios y lista de precios.
AuthModule: Módulo dedicado al inicio de sesión y registro (Google Auth).
DashboardModule: Área privada para clientes y administradores.
[NEW] Integración HTTP (Consumo de API)
En lugar de usar el fetch nativo dentro de un script de Javascript puro (como tu actual main.js), se utilizará el robusto HttpClientModule de Angular para consumir los URIs de NestJS:
Creación de AppointmentsService para realizar llamadas (GET, POST, PUT, DELETE) a tu nuevo servidor NestJS.
Creación de AuthService para manejar el estado de la sesión global utilizando RxJS (Observables), reemplazando el sessionStorage manual.
3. Backend API (NestJS + TypeScript)
El Backend dejará de renderizar y enviar código HTML/CSS. Su única función será exponer endpoints (URIs) consumibles.
[NEW] Controladores REST (URIs CRUD)
Se generarán URIs independientes para cada entidad de la base de datos (CRUD) y procesos extra (Autenticación):
Procesos Extra (Autenticación):
POST /api/auth/login
POST /api/auth/register
CRUD de Citas (Appointments):
GET /api/appointments (Leer todas las citas)
GET /api/appointments/:id (Leer una cita)
POST /api/appointments (Crear cita)
PUT /api/appointments/:id (Modificar cita)
DELETE /api/appointments/:id (Cancelar cita)
CRUD de Servicios (Services):
GET /api/services
POST /api/services (etc...)
[NEW] Servicios y Base de Datos (Supabase/PostgreSQL)
Configuración de conexión segura a la base de datos usando variables de entorno (.env).
Implementación de JWT validation para asegurar que solo los usuarios autenticados consuman el CRUD.
