provider "google" {
    credentials = "${file("mygcp-test-project-001-f9b004e6a0b0.json")}"
    project = "${var.cloud_project_id}"
    region = "${var.region}"
}
