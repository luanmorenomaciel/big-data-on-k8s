{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "name" -}}
{{- default .Chart.Name .Values.nameOverride -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 24 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "fullname" -}}
{{- printf "%s" .Release.Name -}}
{{- end -}}

{{- define "metricTopic" -}}
{{- if .Values.lenses.topics.suffix -}}
_kafka_lenses_metrics_{{ .Values.lenses.topics.suffix }}
{{- else -}}
_kafka_lenses_metrics
{{- end -}}
{{- end -}}

{{- define "auditTopic" -}}
{{- if .Values.lenses.topics.suffix -}}
_kafka_lenses_audits_{{ .Values.lenses.topics.suffix }}
{{- else -}}
_kafka_lenses_audits
{{- end -}}
{{- end -}}

{{- define "processorTopic" -}}
{{- if .Values.lenses.topics.suffix -}}
_kafka_lenses_processors_{{ .Values.lenses.topics.suffix }}
{{- else -}}
_kafka_lenses_processors
{{- end -}}
{{- end -}}

{{- define "alertTopic" -}}
{{- if .Values.lenses.topics.suffix -}}
_kafka_lenses_alerts_{{ .Values.lenses.topics.suffix }}
{{- else -}}
_kafka_lenses_alerts
{{- end -}}
{{- end -}}

{{- define "profileTopic" -}}
{{- if .Values.lenses.topics.suffix -}}
_kafka_lenses_profiles_{{ .Values.lenses.topics.suffix }}
{{- else -}}
_kafka_lenses_profiles
{{- end -}}
{{- end -}}

{{- define "alertSettingTopic" -}}
{{- if .Values.lenses.topics.suffix -}}
_kafka_lenses_alert_settings_{{ .Values.lenses.topics.suffix }}
{{- else -}}
_kafka_lenses_alert_settings
{{- end -}}
{{- end -}}

{{- define "clusterTopic" -}}
{{- if .Values.lenses.topics.suffix -}}
_kafka_lenses_cluster_{{ .Values.lenses.topics.suffix }}
{{- else -}}
_kafka_lenses_cluster
{{- end -}}
{{- end -}}

{{- define "lsqlTopic" -}}
{{- if .Values.lenses.topics.suffix -}}
_kafka_lenses_lsql_storage_{{ .Values.lenses.topics.suffix }}
{{- else -}}
_kafka_lenses_lsql_storage
{{- end -}}
{{- end -}}

{{- define "metadataTopic" -}}
{{- if .Values.lenses.topics.suffix -}}
_kafka_lenses_topics_metadata_{{ .Values.lenses.topics.suffix }}
{{- else -}}
_kafka_lenses_topics_metadata
{{- end -}}
{{- end -}}

{{- define "topologyTopic" -}}
{{- if .Values.lenses.topics.suffix -}}
__topology_{{ .Values.lenses.topics.suffix }}
{{- else -}}
__topology
{{- end -}}
{{- end -}}

{{- define "externalMetricsTopic" -}}
{{- if .Values.lenses.topics.suffix -}}
__topology__metrics_{{ .Values.lenses.topics.suffix }}
{{- else -}}
__topology__metrics
{{- end -}}
{{- end -}}

{{- define "connectorsTopic" -}}
{{- if .Values.lenses.topics.suffix -}}
_kafka_lenses_connectors_{{ .Values.lenses.topics.suffix }}
{{- else -}}
_kafka_lenses_processors
{{- end -}}
{{- end -}}

{{- define "securityProtocol" -}}
{{- if and .Values.lenses.kafka.sasl.enabled .Values.lenses.kafka.ssl.enabled -}}
SASL_SSL
{{- end -}}
{{- if and .Values.lenses.kafka.sasl.enabled (not .Values.lenses.kafka.ssl.enabled) -}}
SASL_PLAINTEXT
{{- end -}}
{{- if and .Values.lenses.kafka.ssl.enabled (not .Values.lenses.kafka.sasl.enabled) -}}
SSL
{{- end -}}
{{- if and (not .Values.lenses.kafka.ssl.enabled) (not .Values.lenses.kafka.sasl.enabled) -}}
PLAINTEXT
{{- end -}}
{{- end -}}

{{- define "bootstrapBrokers" -}}
{{- $protocol := include "securityProtocol" . -}}
{{ range $index, $element := .Values.lenses.kafka.bootstrapServers }}
  {{- if $index -}}
    {{- if eq $protocol "PLAINTEXT" -}}
  ,{{$protocol}}://{{$element.name}}:{{$element.port}}
    {{- end -}}
    {{- if eq $protocol "SSL" -}}
  ,{{$protocol}}://{{$element.name}}:{{$element.sslPort}}
    {{- end -}}
    {{- if eq $protocol "SASL_SSL" -}}
  ,{{$protocol}}://{{$element.name}}:{{$element.saslSslPort}}
    {{- end -}}
    {{- if eq $protocol "SASL_PLAINTEXT" -}}
  ,{{$protocol}}://{{$element.name}}:{{$element.saslPlainTextPort}}
    {{- end -}}
  {{- else -}}
    {{- if eq $protocol "PLAINTEXT" -}}
  {{$protocol}}://{{$element.name}}:{{$element.port}}
    {{- end -}}
    {{- if eq $protocol "SSL" -}}
  {{$protocol}}://{{$element.name}}:{{$element.sslPort}}
    {{- end -}}
    {{- if eq $protocol "SASL_SSL" -}}
  {{$protocol}}://{{$element.name}}:{{$element.saslSslPort}}
    {{- end -}}
    {{- if eq $protocol "SASL_PLAINTEXT" -}}
  {{$protocol}}://{{$element.name}}:{{$element.saslPlainTextPort}}
    {{- end -}}
  {{- end -}}
  {{end}}
{{- end -}}

{{- define "kafkaMetrics" -}}
{{- if and .Values.lenses.kafka.metrics .Values.lenses.kafka.metrics.enabled -}}
{
  type: {{ default "JMX" .Values.lenses.kafka.metrics.type | quote}},
  ssl: {{ default false .Values.lenses.kafka.metrics.ssl}},
  {{- if .Values.lenses.kafka.metrics.username}}
  user: {{ .Values.lenses.kafka.metrics.username | quote}},
  {{- end }}
  {{- if .Values.lenses.kafka.metrics.password}}
  password: {{ .Values.lenses.kafka.metrics.password | quote}},
  {{- end }}
  {{- if .Values.lenses.kafka.metrics.ports}}
  port: [
    {{- range $portIndex, $portDetails := .Values.lenses.kafka.metrics.ports }}
    {{- if $portIndex -}},{{- end }}
    {
      {{- range $key, $value := $portDetails }}
      {{ $key }}: {{ $value | quote }},
      {{- end}}
    }
    {{- end}}
  ]
  {{- else}}
  default.port: {{ .Values.lenses.kafka.metrics.port }}
  {{- end}}
}
{{- end -}}
{{- end -}}

{{- define "kafkaSchemaBasicAuth" -}}
  {{- if and .Values.lenses.schemaRegistries.security.enabled .Values.lenses.schemaRegistries.security.authType -}}
    {{- if eq ((.Values.lenses.schemaRegistries.security | default (dict "authType" "")).authType) "USER_INFO" -}}
      {{- required "When Schema registry security auth type is USER_INFO then username should be provided." .Values.lenses.schemaRegistries.security.username -}}:{{- required "When Schema registry security auth type is USER_INFO then password should be provided." .Values.lenses.schemaRegistries.security.password -}}
    {{- end -}}
  {{- end -}}
{{- end -}}

{{- define "jmxBrokers" -}}
[
  {{ range $index, $element := .Values.lenses.kafka.jmxBrokers }}
  {{- if not $index -}}{id: {{$element.id}}, port: {{$element.port}}}
  {{- else}},
  {id: {{$element.id}}, port: {{$element.port}}}
  {{- end}}
{{- end}}
]
{{- end -}}

{{- define "zookeepers" -}}
{{- if .Values.lenses.zookeepers.enabled -}}
[
  {{ range $index, $element := .Values.lenses.zookeepers.hosts }}
  {{- if not $index -}}{url: "{{$element.host}}:{{$element.port}}"
  {{- if $element.metrics -}}, metrics: {
    {{- if eq $element.metrics.type "JMX" -}}
    url: "{{$element.host}}:{{$element.metrics.port}}",
    {{- else }}
    url: "{{$element.protocol}}://{{$element.host}}:{{$element.metrics.port}}",
    {{- end }}
    type: "{{$element.metrics.type}}",
    ssl: {{default false $element.metrics.ssl}},
    {{- if $element.metrics.username -}}
    user: {{$element.metrics.username | quote}},
    {{- end }}
    {{- if $element.metrics.password -}}
    password: {{$element.metrics.password | quote}},
    {{- end }}
  }{{- end}}}
  {{- else}},
  {url: "{{$element.host}}:{{$element.port}}"
  {{- if $element.metrics -}}, metrics: {
    {{- if eq $element.metrics.type "JMX" -}}
    url: "{{$element.host}}:{{$element.metrics.port}}",
    {{- else }}
    url: "{{$element.protocol}}://{{$element.host}}:{{$element.metrics.port}}",
    {{- end }}
    type: "{{default "JMX" $element.metrics.type}}",
    ssl: {{default false $element.ssl}},
    {{- if $element.metrics.username -}}
    user: {{$element.metrics.username | quote}},
    {{- end }}
    {{- if $element.metrics.password -}}
    password: {{$element.metrics.password | quote}}
    {{- end }}
  }{{- end}}}
  {{- end}}
{{- end}}
]
{{- end -}}
{{- end -}}

{{- define "registries" -}}
{{- if .Values.lenses.schemaRegistries.enabled -}}
[
  {{ range $index, $element := .Values.lenses.schemaRegistries.hosts }}
  {{- if not $index -}}{url: "{{$element.protocol}}://{{$element.host}}:{{$element.port}}{{$element.path}}"
  {{- if $element.metrics -}}, metrics: {
    {{- if eq $element.metrics.type "JMX" -}}
    url: "{{$element.host}}:{{$element.metrics.port}}",
    {{- else }}
    url: "{{$element.protocol}}://{{$element.host}}:{{$element.metrics.port}}",
    {{- end }}
    type: "{{default "JMX" $element.metrics.type}}",
    ssl: {{default false $element.metrics.ssl}}
    {{- if $element.metrics.username -}},
    user: {{$element.metrics.username | quote}},
    {{- end }}
    {{- if $element.metrics.password -}}
    password: {{$element.metrics.password | quote}}
    {{- end }}
  }{{- end}}}
  {{- else}},
  {url: "{{$element.protocol}}://{{$element.host}}:{{$element.port}}"
  {{- if $element.metrics -}}, metrics: {
    {{- if eq $element.metrics.type "JMX" -}}
    url: "{{$element.host}}:{{$element.metrics.port}}",
    {{- else }}
    url: "{{$element.protocol}}://{{$element.host}}:{{$element.metrics.port}}",
    {{- end }}
    type: "{{default "JMX" $element.metrics.type}}",
    ssl: {{default false $element.ssl}}
    {{- if $element.metrics.username -}},
    user: {{$element.metrics.username | quote}},
    {{- end }}
    {{- if $element.metrics.password -}}
    password: {{$element.metrics.password | quote}}
    {{- end }}
  }{{- end}}}
  {{- end}}
{{- end}}
]
{{- end -}}
{{- end -}}


{{- define "connect" -}}
{{- if .Values.lenses.connectClusters.enabled -}}
[
{{- range $clusterCount, $cluster := .Values.lenses.connectClusters.clusters -}}
  {{- $port := $cluster.port -}}
  {{- $protocol := $cluster.protocol -}}
  {{- if $clusterCount }},{{ end }}
  {
    name: {{ $cluster.name | quote }},
    statuses: {{ $cluster.statusTopic | quote }},
    configs: {{ $cluster.configTopic | quote }},
    offsets: {{ $cluster.offsetsTopic | quote }},
    {{ if $cluster.authType }}auth: {{ $cluster.authType | quote }},
    {{ end -}}
    {{ if $cluster.username }}username: {{ $cluster.username | quote }},
    {{ end -}}
    {{ if $cluster.password }}password: {{ $cluster.password | quote }},
    {{ end -}}
    {{ if $cluster.aes256 }}aes256:
      {{- range $value := $cluster.aes256 -}}
        {{- if $value.key }} { key: {{$value.key | quote}} },{{- end -}}
      {{- end }}
    {{ end -}}
    urls: [
      {{ if not $cluster.hosts }}
      {{/* Deliberately fail helm deployment */}}
      {{ required "A connect cluster should always have hosts." nil }}
      {{ end }}
      {{- range $key, $host := $cluster.hosts -}}
      {{- if $key -}},
      {{ end -}}
      {
        url: "{{$protocol}}://{{$host.host}}:{{$port}}"
        {{- if $host.metrics -}},
        metrics: {
          {{- if eq $host.metrics.type "JMX" }}
          url: "{{$host.host}}:{{$host.metrics.port}}"
          {{- else }}
          url: "{{$protocol}}://{{$host.host}}:{{$host.metrics.port}}"
          {{- end }},
          type: {{ default "JMX" $host.metrics.type | quote  }},
          ssl: {{ default "false" $host.metrics.ssl }},
          {{- if $host.metrics.username }}
          user: {{$host.metrics.username | quote}},
          {{- end }}
          {{- if $host.metrics.password }}
          password: {{$host.metrics.password | quote}}
          {{- end }}
        }{{- end}}
      }
      {{- end }}
    ]
  }
{{- end}}
]
{{- end -}}
{{- end -}}


{{- define "alertPlugins" -}}
{{- if .Values.lenses.alerts.plugins -}}
[
  {{ range $index, $element := .Values.lenses.alerts.plugins }}
  {{- if not $index -}}{class: "{{$element.class}}", config: {{$element.config}}}
  {{- else}},{class: "{{$element.class}}", config: {{$element.config}}}{{- end }}
  {{- end }}
]
{{- end -}}
{{- end -}}

{{- define "kerberos" -}}
{{- if .Values.lenses.security.kerberos.enabled }}
lenses.security.kerberos.service.principal={{ .Values.lenses.security.kerberos.servicePrincipal | quote }}
lenses.security.kerberos.keytab=/mnt/secrets/lenses.keytab
lenses.security.kerberos.debug={{ .Values.lenses.security.kerberos.debug | quote }}
{{end -}}
{{- end -}}

{{- define "lensesAppendConf" -}}
{{- if .Values.lenses.storage.postgres.enabled }}
lenses.storage.postgres.host={{ required "PostgreSQL 'host' value is mandatory" .Values.lenses.storage.postgres.host | quote }}
lenses.storage.postgres.database={{ required "PostgreSQL 'database' value is mandatory" .Values.lenses.storage.postgres.database | quote }}
lenses.storage.postgres.username={{ required "PostgreSQL 'username' value is mandatory" .Values.lenses.storage.postgres.username | quote }}
{{- if .Values.lenses.storage.postgres.port }}
lenses.storage.postgres.port={{  .Values.lenses.storage.postgres.port | quote }}
{{- end }}
{{- if .Values.lenses.storage.postgres.schema }}
lenses.storage.postgres.schema={{ .Values.lenses.storage.postgres.schema | quote }}
{{- end }}
{{- end }}
{{- if and .Values.lenses.kafka.sasl.enabled (not .Values.lenses.kafka.sasl.jaasConfig) }}
{{/* Deliberately fail helm deployment if sasl enabled and jaasConfig is missing */}}
{{ required "SASL is enabled but lenses.kafka.sasl.jaasConfig is not set." nil }}
{{- end }}
{{- if and .Values.lenses.kafka.sasl.enabled .Values.lenses.kafka.sasl.jaasConfig }}
lenses.kafka.settings.client.sasl.jaas.config="""{{ .Values.lenses.kafka.sasl.jaasConfig }}
"""
{{- end }}
{{ default "" .Values.lenses.append.conf }}
{{- end -}}

{{- define "securityConf" -}}
{{- if .Values.lenses.security.defaultUser -}}
lenses.security.user={{ .Values.lenses.security.defaultUser.username | quote }}
lenses.security.password={{ .Values.lenses.security.defaultUser.password | quote }}
{{- end -}}
{{- if .Values.lenses.security.ldap.enabled }}
lenses.security.ldap.url={{ .Values.lenses.security.ldap.url | quote }}
lenses.security.ldap.base={{ .Values.lenses.security.ldap.base | quote }}
lenses.security.ldap.user={{ .Values.lenses.security.ldap.user | quote }}
lenses.security.ldap.password={{ .Values.lenses.security.ldap.password | quote }}
lenses.security.ldap.filter={{ .Values.lenses.security.ldap.filter | quote }}
lenses.security.ldap.plugin.class={{ .Values.lenses.security.ldap.plugin.class | quote }}
lenses.security.ldap.plugin.memberof.key={{ .Values.lenses.security.ldap.plugin.memberofKey | quote }}
lenses.security.ldap.plugin.group.extract.regex={{ .Values.lenses.security.ldap.plugin.groupExtractRegex | quote }}
lenses.security.ldap.plugin.person.name.key={{ .Values.lenses.security.ldap.plugin.personNameKey | quote }}
{{- end -}}
{{- if .Values.lenses.security.saml.enabled }}
lenses.security.saml.base.url={{ .Values.lenses.security.saml.baseUrl | quote }}
lenses.security.saml.idp.provider={{ .Values.lenses.security.saml.provider | quote }}
lenses.security.saml.idp.metadata.file="/mnt/secrets/saml.idp.xml"
lenses.security.saml.keystore.location="/mnt/secrets/saml.keystore.jks"
lenses.security.saml.keystore.password={{ .Values.lenses.security.saml.keyStorePassword | quote }}
{{- if .Values.lenses.security.saml.keyAlias }}
lenses.security.saml.key.alias={{ .Values.lenses.security.saml.keyAlias | quote }}
{{- end }}
lenses.security.saml.key.password={{ .Values.lenses.security.saml.keyPassword | quote }}
{{- end }}
{{- if .Values.lenses.security.kerberos.enabled -}}
{{ include "kerberos" .}}
{{- end -}}
{{- if .Values.lenses.storage.postgres.enabled }}
lenses.storage.postgres.password={{ required "PostgreSQL 'password' value is mandatory" .Values.lenses.storage.postgres.password | quote }}
{{- end -}}
{{- end -}}

{{/*
Return the appropriate apiVersion for ingress.
*/}}
{{- define "ingress.apiVersion" -}}
{{- if .Capabilities.APIVersions.Has "networking.k8s.io/v1beta1" -}}
{{- print "networking.k8s.io/v1beta1" -}}
{{- else -}}
{{- print "extensions/v1beta1" -}}
{{- end -}}
{{- end -}}
