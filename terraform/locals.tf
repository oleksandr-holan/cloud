locals {
  _url_without_protocol_list = split("://", var.github_repo)
  _host_and_path             = element(local._url_without_protocol_list, 1)
  _path_parts                = split("/", local._host_and_path)

  github = {
    host  = element(local._path_parts, 0)
    owner = element(local._path_parts, 1)
    repo  = element(local._path_parts, 2)
  }
}
