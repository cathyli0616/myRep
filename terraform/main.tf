
# Pub-Sub resrouces
resource "google_pubsub_topic" "ccs-billing" {
  project = "${var.cloud_project_id}"
  name    = "${var.topic_name}"
}

resource "google_pubsub_subscription" "ccs-billing-sub2" {
  # Optional
  project = "${var.cloud_project_id}"

  name  = "${var.async_subscription_name}"
  topic = "${google_pubsub_topic.ccs-billing.name}"
}


resource "google_compute_instance_template" "default" {
  name         = "${var.name}-instance-template"
  project      = "${var.cloud_project_id}"
  machine_type = "${var.machine_type}"
  region       = "${var.region}"
  tags         = "${var.tags}"

  disk {
    source_image = "debian-cloud/debian-9"
    auto_delete  = true
    boot         = true    
  }

  network_interface {
    network      = "default"
    access_config {
      // Ephemeral IP
    }
  }

  labels = {
    environment = "dev"
  }

  metadata = {
    foo = "bar"
  }

  service_account {
    scopes = "${var.scopes}"
  }

  lifecycle {
    create_before_destroy = true
  }

}

resource "google_compute_instance_from_template" "default" {
  name = "${var.name}-instance"
  zone = "${var.zone}"

  source_instance_template = "${google_compute_instance_template.default.self_link}"

  can_ip_forward = false
  labels = {
    my_key = "my_value"
  }
}

resource "google_compute_disk" "rs_disk" {
    name = "${var.name}-disk"
    type = "pd-ssd"
    zone = "${var.zone}"
    # If the snapshot is in another project than this disk, you must supply a full URL
    snapshot = "${var.name}-snapshot"
    #if disk from image or snapshot, size should not less than image or snapshot size (GB)
    size = 15
}

resource "google_compute_instance" "rs_vm" {
  name         = "${var.name}-instance-1"
  zone         = "${var.zone}"
  machine_type = "f1-micro"

  boot_disk {
    source      = "${google_compute_disk.rs_disk.self_link}"
    device_name = "${google_compute_disk.rs_disk.name}"
  }

  network_interface {
	  network = "default"
    access_config {
      // Ephemeral IP
    }
  }
}