🦈 SharkHub Barbershop Management - API RESTful SpecificationEste documento contiene la especificación de diseño técnico detallada para la API RESTful de SharkHub. Se estructuran todos los endpoints mapeados desde las rutas de Laravel, clasificados por módulos de recursos y por roles del sistema.📌 1. Información General y Configuración de BaseProyecto: SharkHub Barbershop Management.Grupo de Trabajo: Ricardo Monge, Alejandro Obando, Gabriel Molina (Universidad de las Fuerzas Armadas ESPE).Base URL: {{base_url}} (Dominio del despliegue de Laravel).Autenticación: Gestionada a través de sesiones nativas de Laravel y llamadas integradas con Supabase Auth.Roles de Acceso: - Público / Visitante: Rutas de registro y login.Cliente (customer): Reservas de citas, búsqueda de servicios y consulta de disponibilidades.Barbero (barber): Creación de servicios y productos, gestión de su agenda de citas.Dueño (owner): Control total de la barbería, asignación de personal, estatus y control global de la agenda.

🔑 2. Módulo de Autenticación y Sesiones

Registrar Cliente
Ruta: POST {{base_url}}/api/auth/registerHeaders: Content-Type: application/jsonRequest Body:{
  "name": "Juan Pérez",
  "email": "juan.perez@email.com",
  "username": "juanperez",
  "password": "password123"
}
Respuesta Esperada (201 Created):{
  "message": "Usuario registrado exitosamente",
  "user": {
    "id": "usr_98234",
    "name": "Juan Pérez",
    "email": "juan.perez@email.com",
    "username": "juanperez"
  }
}
Iniciar Sesión de UsuarioRuta: POST {{base_url}}/api/auth/loginHeaders: Content-Type: application/jsonRequest Body:{
  "email": "juan.perez@email.com",
  "password": "password123"
}
Respuesta Esperada (200 OK o 201 Created):{
  "message": "Sesión iniciada correctamente",
  "token": "1|laravel_sanctum_token_hash_here",
  "user": {
    "id": "usr_98234",
    "name": "Juan Pérez",
    "email": "juan.perez@email.com"
  }
}
👥 3. Módulo de Usuarios (/api/users)Obtener Lista de UsuariosRuta: GET {{base_url}}/api/usersRespuesta Esperada (200 OK):[
  {
    "id": "usr_001",
    "full_name": "Ricardo Monge",
    "email": "ricardo@email.com",
    "phone": "0999888777"
  },
  {
    "id": "usr_002",
    "full_name": "Alejandro Obando",
    "email": "alejandro@email.com",
    "phone": "0999555444"
  }
]
Obtener Perfil del Usuario AutenticadoRuta: GET {{base_url}}/api/users/meRespuesta Esperada (200 OK):{
  "id": "usr_001",
  "full_name": "Ricardo Monge",
  "email": "ricardo@email.com",
  "phone": "0999888777",
  "role": "owner"
}
Crear Nuevo UsuarioRuta: POST {{base_url}}/api/usersRequest Body:{
  "full_name": "Gabriel Molina",
  "email": "gabriel@email.com",
  "password": "securepassword789"
}
Respuesta Esperada (201 Created):{
  "id": "usr_003",
  "full_name": "Gabriel Molina",
  "email": "gabriel@email.com",
  "created_at": "2026-05-24T15:30:00Z"
}
Obtener Detalle de un Usuario EspecíficoRuta: GET {{base_url}}/api/users/{user_id}Parámetros de Ruta: user_id (ID único del usuario).Respuesta Esperada (200 OK):{
  "id": "usr_003",
  "full_name": "Gabriel Molina",
  "email": "gabriel@email.com",
  "phone": "0987654321"
}
Actualizar un UsuarioRuta: PUT {{base_url}}/api/users/{user_id}Parámetros de Ruta: user_id (ID del usuario).Request Body:{
  "full_name": "Gabriel Molina Actualizado",
  "phone": "0998765432"
}
Respuesta Esperada (200 OK):{
  "id": "usr_003",
  "full_name": "Gabriel Molina Actualizado",
  "phone": "0998765432",
  "updated_at": "2026-05-24T16:00:00Z"
}
Eliminar UsuarioRuta: DELETE {{base_url}}/api/users/{user_id}Respuesta Esperada (204 No Content): (Cuerpo vacío)⏱️ 4. Módulo de Gestión de Sesiones (/api/sessions)Crear Sesión (Login de API)Ruta: POST {{base_url}}/api/sessionsRequest Body:{
  "email": "gabriel@email.com",
  "password": "securepassword789"
}
Respuesta Esperada (201 Created):{
  "token": "2|session_token_example_xyz",
  "expires_at": "2026-06-24T18:50:00Z"
}
Consultar Sesión Actual ActivaRuta: GET {{base_url}}/api/sessions/currentRespuesta Esperada (200 OK):{
  "user_id": "usr_003",
  "full_name": "Gabriel Molina Actualizado",
  "session_active": true
}
Cerrar Sesión Actual (Logout)Ruta: DELETE {{base_url}}/api/sessions/currentRespuesta Esperada (204 No Content): (Cuerpo vacío, sesión invalidada en Laravel)💈 5. Módulo de Barberías (/api/barbershops)Listar Barberías en la PlataformaRuta: GET {{base_url}}/api/barbershopsRespuesta Esperada (200 OK):[
  {
    "id": "shop_101",
    "name": "SharkHub Barberia Central",
    "address": "Av. General Rumiñahui, Sangolqui",
    "phone": "022333444"
  }
]
Registrar una Nueva BarberíaRuta: POST {{base_url}}/api/barbershopsRequest Body:{
  "name": "SharkHub Barberia Central",
  "address": "Av. General Rumiñahui, Sangolqui",
  "phone": "022333444"
}
Respuesta Esperada (201 Created):{
  "id": "shop_101",
  "name": "SharkHub Barberia Central",
  "address": "Av. General Rumiñahui, Sangolqui",
  "phone": "022333444",
  "status": "pending_approval"
}
Obtener Detalles de una BarberíaRuta: GET {{base_url}}/api/barbershops/{shop_id}Parámetros de Ruta: shop_id (ID de la barbería).Respuesta Esperada (200 OK):{
  "id": "shop_101",
  "name": "SharkHub Barberia Central",
  "address": "Av. General Rumiñahui, Sangolqui",
  "phone": "022333444",
  "description": "Estilo y elegancia de vanguardia."
}
Actualizar Información de una BarberíaRuta: PUT {{base_url}}/api/barbershops/{shop_id}Parámetros de Ruta: shop_idRequest Body:{
  "name": "SharkHub Master Cut",
  "description": "Cortes modernos y barbería clásica tradicional"
}
Respuesta Esperada (200 OK):{
  "id": "shop_101",
  "name": "SharkHub Master Cut",
  "description": "Cortes modernos y barbería clásica tradicional",
  "updated_at": "2026-05-24T17:00:00Z"
}
Eliminar / Desactivar BarberíaRuta: DELETE {{base_url}}/api/barbershops/{shop_id}Respuesta Esperada (204 No Content)👥 6. Miembros de Barbería (/api/barbershops/{shop_id}/members)Listar Miembros de una BarberíaRuta: GET {{base_url}}/api/barbershops/{shop_id}/membersRespuesta Esperada (200 OK):[
  {
    "member_id": "mem_201",
    "user_id": "usr_002",
    "name": "Alejandro Obando",
    "role": "barber",
    "status": "active"
  }
]
Agregar un Miembro a la BarberíaRuta: POST {{base_url}}/api/barbershops/{shop_id}/membersRequest Body:{
  "user_id": "usr_002",
  "role": "barber"
}
Respuesta Esperada (201 Created):{
  "member_id": "mem_201",
  "user_id": "usr_002",
  "role": "barber",
  "status": "pending_confirmation"
}
Consultar Detalles de un MiembroRuta: GET {{base_url}}/api/barbershops/{shop_id}/members/{member_id}Respuesta Esperada (200 OK):{
  "member_id": "mem_201",
  "user_id": "usr_002",
  "name": "Alejandro Obando",
  "role": "barber",
  "status": "active",
  "joined_at": "2026-05-24"
}
Actualizar Rol o Estado de un MiembroRuta: PUT {{base_url}}/api/barbershops/{shop_id}/members/{member_id}Request Body:{
  "status": "active",
  "role": "owner"
}
Respuesta Esperada (200 OK):{
  "member_id": "mem_201",
  "role": "owner",
  "status": "active"
}
Remover un Miembro de la BarberíaRuta: DELETE {{base_url}}/api/barbershops/{shop_id}/members/{member_id}Respuesta Esperada (204 No Content)💇‍♂️ 7. Módulo de Servicios (/api/barbershops/{shop_id}/services)Listar Servicios de una BarberíaRuta: GET {{base_url}}/api/barbershops/{shop_id}/servicesRespuesta Esperada (200 OK):[
  {
    "service_id": "srv_301",
    "name": "Corte de Cabello",
    "price": 10.0,
    "is_active": true
  }
]
Crear un Servicio en la BarberíaRuta: POST {{base_url}}/api/barbershops/{shop_id}/servicesRequest Body:{
  "name": "Corte",
  "price": 10.0
}
Respuesta Esperada (201 Created):{
  "service_id": "srv_301",
  "name": "Corte",
  "price": 10.0,
  "is_active": true
}
Obtener Detalle de un ServicioRuta: GET {{base_url}}/api/barbershops/{shop_id}/services/{service_id}Respuesta Esperada (200 OK):{
  "service_id": "srv_301",
  "name": "Corte",
  "price": 10.0,
  "is_active": true,
  "description": "Corte clásico moderno para caballero"
}
Actualizar Precio y Estado del ServicioRuta: PUT {{base_url}}/api/barbershops/{shop_id}/services/{service_id}Request Body:{
  "price": 12.0,
  "is_active": true
}
Respuesta Esperada (200 OK):{
  "service_id": "srv_301",
  "price": 12.0,
  "is_active": true
}
Eliminar / Deshabilitar un ServicioRuta: DELETE {{base_url}}/api/barbershops/{shop_id}/services/{service_id}Respuesta Esperada (204 No Content)🧴 8. Módulo de Productos (/api/barbershops/{shop_id}/products)Listar Productos de una BarberíaRuta: GET {{base_url}}/api/barbershops/{shop_id}/productsRespuesta Esperada (200 OK):[
  {
    "product_id": "prd_401",
    "name": "Gel de Fijación Extrema",
    "stock": 50,
    "price": 8.0
  }
]
Agregar un Producto al InventarioRuta: POST {{base_url}}/api/barbershops/{shop_id}/productsRequest Body:{
  "name": "Gel",
  "stock": 50
}
Respuesta Esperada (201 Created):{
  "product_id": "prd_401",
  "name": "Gel",
  "stock": 50,
  "price": 0.0
}
Obtener Detalle de un ProductoRuta: GET {{base_url}}/api/barbershops/{shop_id}/products/{product_id}Respuesta Esperada (200 OK):{
  "product_id": "prd_401",
  "name": "Gel",
  "stock": 50,
  "price": 8.0,
  "description": "Fijación premium para peinado largo"
}
Actualizar Stock y Precio del ProductoRuta: PUT {{base_url}}/api/barbershops/{shop_id}/products/{product_id}Request Body:{
  "stock": 45,
  "price": 8.0
}
Respuesta Esperada (200 OK):{
  "product_id": "prd_401",
  "stock": 45,
  "price": 8.0
}
Eliminar Producto del CatálogoRuta: DELETE {{base_url}}/api/barbershops/{shop_id}/products/{product_id}Respuesta Esperada (204 No Content)📅 9. Módulo de Citas (/api/appointments)Listar Citas Registradas en el SistemaRuta: GET {{base_url}}/api/appointmentsRespuesta Esperada (200 OK):[
  {
    "appointment_id": "apt_501",
    "barber_id": "usr_002",
    "client_id": "usr_003",
    "appointment_date": "2026-05-25",
    "status": "pending"
  }
]
Crear una Nueva Cita (Reserva)Ruta: POST {{base_url}}/api/appointmentsRequest Body:{
  "barber_id": "usr_002",
  "client_id": "usr_003",
  "date": "2026-05-25"
}
Respuesta Esperada (201 Created):{
  "appointment_id": "apt_501",
  "barber_id": "usr_002",
  "client_id": "usr_003",
  "appointment_date": "2026-05-25",
  "status": "pending"
}
Obtener Detalles de una CitaRuta: GET {{base_url}}/api/appointments/{appointment_id}Respuesta Esperada (200 OK):{
  "appointment_id": "apt_501",
  "barber_id": "usr_002",
  "client_id": "usr_003",
  "appointment_date": "2026-05-25",
  "status": "pending",
  "notes": "Preferencia por corte bajo."
}
Reprogramar o Actualizar CitaRuta: PUT {{base_url}}/api/appointments/{appointment_id}Request Body:{
  "appointment_date": "2026-05-26",
  "status": "confirmed"
}
Respuesta Esperada (200 OK):{
  "appointment_id": "apt_501",
  "appointment_date": "2026-05-26",
  "status": "confirmed"
}
Eliminar / Cancelar CitaRuta: DELETE {{base_url}}/api/appointments/{appointment_id}Respuesta Esperada (204 No Content): (Cita borrada correctamente)🛠️ 10. Servicios Asociados a Citas (/api/appointments/{apt_id}/services)Listar Servicios dentro de una CitaRuta: GET {{base_url}}/api/appointments/{appointment_id}/servicesRespuesta Esperada (200 OK):[
  {
    "service_id": "srv_301",
    "name": "Corte de Cabello",
    "price": 12.0
  }
]
Vincular un Servicio a una CitaRuta: POST {{base_url}}/api/appointments/{appointment_id}/servicesRequest Body:{
  "service_id": "srv_301"
}
Respuesta Esperada (201 Created):{
  "appointment_id": "apt_501",
  "service_id": "srv_301",
  "message": "Servicio agregado a la cita"
}
Obtener Detalle de un Servicio dentro de una CitaRuta: GET {{base_url}}/api/appointments/{appointment_id}/services/{service_id}Respuesta Esperada (200 OK):{
  "appointment_id": "apt_501",
  "service_id": "srv_301",
  "name": "Corte de Cabello",
  "price": 12.0,
  "notes": "Detalle particular para el servicio."
}
Actualizar Notas o Especificaciones de un Servicio en la CitaRuta: PUT {{base_url}}/api/appointments/{appointment_id}/services/{service_id}Request Body:{
  "notes": "Preferencia por corte bajo."
}
Respuesta Esperada (200 OK):{
  "appointment_id": "apt_501",
  "service_id": "srv_301",
  "notes": "Preferencia por corte bajo.",
  "updated_at": "2026-05-24T18:00:00Z"
}
Desvincular un Servicio de la CitaRuta: DELETE {{base_url}}/api/appointments/{appointment_id}/services/{service_id}Respuesta Esperada (204 No Content)📅 11. Disponibilidad de Barberos (/api/barbers/{barber_id}/availabilities)Listar Horarios y Disponibilidades de un BarberoRuta: GET {{base_url}}/api/barbers/{barber_id}/availabilitiesRespuesta Esperada (200 OK):[
  {
    "availability_id": "avb_601",
    "day_of_week": 1,
    "start_time": "08:00",
    "end_time": "17:00"
  }
]
Agregar un Bloque de Horario / DisponibilidadRuta: POST {{base_url}}/api/barbers/{barber_id}/availabilitiesRequest Body:{
  "day_of_week": 1,
  "start_time": "08:00"
}
Respuesta Esperada (201 Created):{
  "availability_id": "avb_601",
  "day_of_week": 1,
  "start_time": "08:00",
  "end_time": "12:00"
}
Obtener Detalles de una Disponibilidad EspecíficaRuta: GET {{base_url}}/api/barbers/{barber_id}/availabilities/{availability_id}Respuesta Esperada (200 OK):{
  "availability_id": "avb_601",
  "day_of_week": 1,
  "start_time": "08:00",
  "end_time": "12:00"
}
Modificar un Bloque de Horario DisponibleRuta: PUT {{base_url}}/api/barbers/{barber_id}/availabilities/{availability_id}Request Body:{
  "end_time": "18:00"
}
Respuesta Esperada (200 OK):{
  "availability_id": "avb_601",
  "day_of_week": 1,
  "start_time": "08:00",
  "end_time": "18:00"
}
Eliminar Bloque de DisponibilidadRuta: DELETE {{base_url}}/api/barbers/{barber_id}/availabilities/{availability_id}Respuesta Esperada (204 No Content)✉️ 12. Códigos de Invitación (/api/barbershops/{shop_id}/invitations)Listar Códigos de Invitación GeneradosRuta: GET {{base_url}}/api/barbershops/{shop_id}/invitationsRespuesta Esperada (200 OK):[
  {
    "invitation_id": "inv_701",
    "code": "SH-982-XYZ",
    "expires_at": "2026-06-01T00:00:00Z",
    "is_active": true
  }
]
Generar un Código de Invitación (Invitación para Barberos)Ruta: POST {{base_url}}/api/barbershops/{shop_id}/invitationsRequest Body:{
  "expires_at": "2026-06-01 00:00:00"
}
Respuesta Esperada (201 Created):{
  "invitation_id": "inv_701",
  "code": "SH-982-XYZ",
  "expires_at": "2026-06-01 00:00:00",
  "is_active": true
}
Obtener Detalle de un Código de InvitaciónRuta: GET {{base_url}}/api/barbershops/{shop_id}/invitations/{invitation_id}Respuesta Esperada (200 OK):{
  "invitation_id": "inv_701",
  "code": "SH-982-XYZ",
  "expires_at": "2026-06-01 00:00:00",
  "is_active": true,
  "created_at": "2026-05-24T18:00:00Z"
}
Desactivar o Modificar Estado de un CódigoRuta: PUT {{base_url}}/api/barbershops/{shop_id}/invitations/{invitation_id}Request Body:{
  "is_active": false
}
Respuesta Esperada (200 OK):{
  "invitation_id": "inv_701",
  "is_active": false
}
Eliminar / Revocar Código de InvitaciónRuta: DELETE {{base_url}}/api/barbershops/{shop_id}/invitations/{invitation_id}Respuesta Esperada (204 No Content)🌍 13. Recursos Globales Adicionales (Público/General)Listar Todos los Barberos del SistemaRuta: GET {{base_url}}/api/barbersRespuesta Esperada (200 OK):[
  {
    "barber_id": "usr_002",
    "name": "Alejandro Obando",
    "specialties": ["Cortes modernos", "Perfilado de barba"]
  }
]
Obtener Detalle de un Barbero EspecíficoRuta: GET {{base_url}}/api/barbers/{barber_id}Respuesta Esperada (200 OK):{
  "barber_id": "usr_002",
  "name": "Alejandro Obando",
  "email": "alejandro@email.com",
  "specialties": ["Cortes modernos", "Perfilado de barba"],
  "rating": 4.9
}
Listar Todos los Servicios Globales en el SistemaRuta: GET {{base_url}}/api/servicesRespuesta Esperada (200 OK):[
  {
    "service_id": "srv_301",
    "name": "Corte de Cabello",
    "average_price": 10.0
  }
]
👑 14. Rutas Especiales por Roles (Dashboard de Negocio)A. Endpoints del Dueño (Owner)Actualizar Perfil de Barbería por el Dueño ActivoRuta: PUT {{base_url}}/api/owner/barbershopRequest Body:{
  "name": "BarberShop Panda Black And White",
  "phone": "0999999999",
  "email": "barbershop@email.com",
  "address": "Sangolqui, Ecuador",
  "description": "Barberia especializada en cortes modernos y clásicos.",
  "logo_url": "[https://example.com/logo.png](https://example.com/logo.png)"
}
Respuesta Esperada (200 OK):{
  "status": "success",
  "message": "Perfil de barbería actualizado correctamente"
}
Añadir un Barbero Registrado a la Barbería del DueñoRuta: POST {{base_url}}/api/owner/barbersRequest Body:{
  "email": "barber@email.com"
}
Respuesta Esperada (200 OK):{
  "message": "Barbero asignado de manera exitosa"
}
Cambiar Estatus de un Miembro BarberoRuta: PATCH {{base_url}}/api/owner/barbers/{member}/statusRequest Body:{
  "status": "active"
}
Nota: Valores aceptados: active, inactive.Filtrar Citas de la Barbería (Consola del Dueño)Ruta: GET {{base_url}}/api/owner/appointmentsQuery Params (Opcionales):date: Fecha en formato YYYY-MM-DD (ej. 2026-05-26).barber_id: ID del barbero asignado.Modificar el Estado de una Reserva de Cita (Dueño)Ruta: PATCH {{base_url}}/api/owner/appointments/{appointment}/statusRequest Body:{
  "status": "confirmed"
}
Nota: Valores aceptados: pending, confirmed, cancelled.B. Endpoints del Barbero (Barber)Filtrar Agenda de Citas del Barbero AutenticadoRuta: GET {{base_url}}/api/barber/appointmentsQuery Params (Opcionales):date: Filtro de fecha en formato YYYY-MM-DD (ej. 2026-05-25).Crear un Nuevo Servicio AsociadoRuta: POST {{base_url}}/api/barber/servicesRequest Body:{
  "barbershop_id": "shop_101",
  "name": "Corte clásico",
  "description": "Servicio de corte de cabello para caballero.",
  "price": 7.5,
  "duration_minutes": 30
}
Registrar un Nuevo Producto en InventarioRuta: POST {{base_url}}/api/barber/productsRequest Body:{
  "barbershop_id": "shop_101",
  "name": "Pomada para cabello",
  "description": "Producto de fijación para peinado.",
  "price": 5.0,
  "stock": 20,
  "image_url": "[https://example.com/product.png](https://example.com/product.png)"
}
C. Endpoints del Cliente (Customer)Buscar y Filtrar Servicios ActivosRuta: GET {{base_url}}/api/customer/servicesQuery Params (Opcionales):barbershop_id: Permite filtrar los servicios disponibles para una sucursal en específico. Si se omite, retorna todo el catálogo global.Consultar Horas de Turno DisponiblesRuta: GET {{base_url}}/api/customer/available-timesQuery Params (Requeridos):barber_id: ID del barbero solicitado.service_id: ID del servicio para estimar duración.date: Fecha seleccionada YYYY-MM-DD (ej. 2026-05-25).Respuesta Esperada (200 OK):{
  "date": "2026-05-25",
  "available_slots": ["09:00", "09:30", "10:00", "11:30", "15:00"]
}
Confirmar Reserva de CitaRuta: POST {{base_url}}/api/customer/appointmentsRequest Body:{
  "barber_id": "usr_002",
  "service_id": "srv_301",
  "appointment_date": "2026-05-25",
  "start_time": "10:00",
  "notes": "Preferencia por corte bajo."
}
Respuesta Esperada (201 Created):{
  "status": "success",
  "message": "Cita agendada de forma correcta",
  "appointment_id": "apt_801"
}
