
variable "cloud_project_id" {
  description = "Google Project id"
  default = "mygcp-test-project-001"
}
# to define a vm location
variable "region" {
  description = "Google Cloud region"
  default = "northamerica-northeast1"
}

variable "zone" {
  description = "Google Cloud zone"
  default = "northamerica-northeast1-a"
}

variable "topic_name" {
  description = "Google Topic name"
  default = "topic-ccs-billing"
}

variable "async_subscription_name" {
  description = "Google aSync subscription name"
  default = "async-pubsub-to-datastore"
}

variable "name" {
  type    = "string"
  default = "sapcc-test"  
}
variable "machine_type" {
  type = "string"
  default = "f1-micro"
}

variable "env" {
  type = "string"
  default = "np"
}

variable "scopes" {
   type = "list" 
   default = ["userinfo-email", "compute-ro", "storage-ro"]
}

variable "tags" {
   type = "list" 
   default = ["foo", "bar"]
}

variable "gce_ssh_user" {
   type = "string" 
   default = "cathy.li@telus.com"
}

variable "gce_ssh_pub_key_file" {
   type = "string" 
   default = "id_rsa.pub"
}

