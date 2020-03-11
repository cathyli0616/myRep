output "instance_template_self_link" {
  value = "${google_compute_instance_template.default.self_link}"
}

output "instance_from_template_self_link" {
  value = "${google_compute_instance_from_template.default.self_link}"
}

output "disk_self_link" {
  value = "${google_compute_disk.rs_disk.self_link}"
}

output "instance_self_link" {
  value = "${google_compute_instance.rs_vm.self_link}"
}
