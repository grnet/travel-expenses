Travel Expenses Stats Visualization
===================================

The travel expenses visualization is implemented by ELK (Elastic Search, Logstash, Kibana) software stack.

Versions
--------

Elastic Search: 2.4.0

Logstash: 5.4.2

Kibana: 4.6.4

Workflow
--------

-	Lostash reads the response of the travel_expenses endpoint:`/api/project/all_project_stats_json/` by using the [http_poller](https://www.elastic.co/guide/en/logstash/current/plugins-inputs-http_poller.html) input plugin. The default configuration of this plugin is the following:

```
http_poller {
    urls => {

      travel_expenses => {

        method => get
        url => "http://localhost:8000/api/project/all_project_stats_json/"

        auth => {
          user => "admin"
          password => "admin"
        }
      }
    }
    request_timeout => 60
    # Supports "cron", "every", "at" and "in" schedules by rufus scheduler
     schedule => { cron => "* * * * * UTC"}
  }
```

One has to change the **url** in order to look at the right endpoint, the **auth** info and finally the **schedule** which follows a crontab like configuration.

-	Casts the various date related fields to a specific date format.

-	Stores the info to Elastic Search backend. One has to set the **hosts** fields and the **template** path

Start logstash with the following command (elastic search should already be running):

```bash
cd visualizations/logstash-5.4-2/;
bin/logstash -f conf/travel_expenses.conf
```

Elastic Search
--------------

Elastic Search and Kibana are configured and started through the following docker-compose image (visualizations/es_kibana/docker-compose.yml):

```
es:
  image: elasticsearch:2.4.0
  ports:
    - "9200:9200"
  environment:
    - http.host=0.0.0.0
    - transport.host=127.0.0.1
kibana:
  image: kibana:4.6.4
  ports:
    - "5601:5601"
  links:
    - es
  environment:
    - ELASTICSEARCH_URL=http://es:9200
```

In order to start it run ([docker-compose](https://docs.docker.com/compose/install/) should be installed):

`docker-compose up`

Kibana
------

After starting the docker-compose image, one has to:

1.	Configure the elastic search index to look for (settings/Index name or pattern): `travel_expenses`

2.	Load the Kibana dashboards(settings/objects/Import) located at: `visualizations/kibana_travel.json`
