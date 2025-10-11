variable "yc_token" {
  description = "OAuth токен Яндекс.Облака"
  type        = string
  sensitive   = true
}

variable "yc_cloud_id" {
  description = "ID облака Yandex.Cloud"
  type        = string
}

variable "yc_folder_id" {
  description = "ID каталога Yandex.Cloud"
  type        = string
}

variable "yc_zone" {
  description = "Зона размещения"
  type        = string
  default     = "ru-central1-a"
}

variable "yc_image_id" {
  description = "ID образа Ubuntu 22.04"
  type        = string
  default     = "fd8v9q9j8gks7g2d7t3h" # Проверенный публичный ID Ubuntu 22.04 LTS
}
