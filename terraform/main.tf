terraform {
  required_version = ">= 1.0.0"
}
resource "local_file" "reporte_infraestructura" {
  content  = "Entorno DataOps Local Preparado de forma Nativa por Cristofer\\nEstado: Operativo\\nFecha de Auditoria: June 2026"
  filename = "${path.module}/estado_infraestructura.txt"
}
output "resultado_despliegue" {
  value = "Infraestructura local desplegada con exito de forma nativa"
}
