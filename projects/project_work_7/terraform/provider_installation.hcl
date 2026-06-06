provider_installation {
  filesystem_mirror {
    path    = "~/.terraform.d/plugins"
  }
  direct {
    exclude = ["yandex-cloud/yandex"]
  }
}
