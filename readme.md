# HA Telemeter

This repository contains a minimal Flask application that allows reading your Telemeter data and exposing it through a simple API. This API can easily be integrated with Home Assistant to add your Telemeter information to your dashboards or automations.

## Installation

The application is available as a Docker image.

It requires your Telenet credentials via ENV variables:

- `TELENET_USERNAME`
- `TELENET_PASSWORD`

The Docker container exposes the API through port `5000` and you can map that to whatever you want.

## Home Assistant Configuration

Add the following sensor to your sensor.yaml file:

``` yaml
- platform: rest
  name: Telenet Telemeter
  unique_id: telenet_telemeter
  state_class: total_increasing
  unit_of_measurement: GB
  json_attributes:
    - period_start
    - period_end
    - product
    - usage_peak
    - usage_offpeak
    - total_usage
  resource: http://192.168.0.186:5000/
  value_template: "{{ '%0.2f' | format(value_json.total_usage / 1000000 | float) }}"
  icon: mdi:network-pos
  scan_interval: 300
```

To split out the attributes into separate sensors, add this to your template.yaml:

``` yaml
- sensor:
  - name: "Telenet Telemeter Total Usage"
    unit_of_measurement: "GB"
    state_class: total_increasing
    state: "{{ '%0.2f' | format(state_attr('telenet_telemeter', 'total_usage') / 1000000 | float) }}"
  - name: "Telenet Telemeter Peak Usage"
    unit_of_measurement: "GB"
    state_class: total_increasing
    state: "{{ '%0.2f' | format(state_attr('telenet_telemeter', 'usage_peak') / 1000000 | float) }}"
  - name: "Telenet Telemeter Off-Peak Usage"
    unit_of_measurement: "GB"
    state_class: total_increasing
    state: "{{ '%0.2f' | format(state_attr('telenet_telemeter', 'usage_offpeak') / 1000000 | float) }}"
```
