Travel Expenses Statistics Visualization Module
===============================================

The travel expenses visualization is implemented using the ELK (Elastic Search, Logstash, Kibana) software stack.

Versions
--------

Elastic Search: 2.4.0

Logstash: 5.4.2

Kibana: 4.6.4

Workflow
--------

-	Lostash reads the response of the travel_expenses endpoint:`/api/project/stats/` by using the [http_poller](https://www.elastic.co/guide/en/logstash/current/plugins-inputs-http_poller.html) input plugin. The default configuration of this plugin is the following:

```
http_poller {
    urls => {

      travel_expenses => {

        method => get
        url => "http://localhost:8000/api/project/stats/"

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

One has to change the **url** in order to look at the right endpoint, the **auth** info and finally the **schedule** which follows a crontab like configuration. The **auth** should be configured based on a travel expenses user who has permissions to read the specific endpoint. The user must be either an **ADMIN or CONTROLLER** user.

-	Casts the various date related fields to a specific date format.

```
filter {
date {
   target => "depart_date"
   match => [ "depart_date", "yyyy-M-d'T'H:m:s" ]

  }
date {
   target => "return_date"
    match => [ "return_date", "yyyy-M-d'T'H:m:s" ]
  }
date {
   target => "task_end_date"
    match => [ "task_end_date", "yyyy-M-d'T'H:m:s" ]
  }
date {
    target => "task_start_date"
    match => [ "task_start_date", "yyyy-M-d'T'H:m:s" ]
  }


}

```

-	Stores the info to Elastic Search backend.

```
output {

elasticsearch {
    hosts => ["http://127.0.0.1:9200"]
    index => "travel_expenses"
    template => "/config-dir/template.json"
    document_id => "%{task_start_date}:%{project}:%{arrival_point}:%{last_name}"
  }
}
```

One has to change the **hosts** to depict the address of elasticsearch backend and also define the path of the template.json file.

The logstash conf file is located at: `/travelsBackend/visualizations/confs/travel_expenses.conf`

The template.json file is located at : `/travelsBackend/visualizations/confs/template.json`

Elastic Search
--------------

Elastic Search is used as the backend store for Travel Expenses visualizations module. The minimum requirement for elastic search configuration is to set the `network.host` in order to be visible by logstash (in our case 127.0.0.1)

Kibana
------

Kibana sits on top of elastic search and is used for visualizing the stats stored at the backend.

#### Minimum setup for Kibana

```
# The host to bind the server to.
server.host: "127.0.0.1"

# If you are running kibana behind a proxy, and want to mount it at a path,
# specify that path here. The basePath can't end in a slash.
server.basePath: "/analytics"

# The Elasticsearch instance to use for all your queries.
elasticsearch.url: "http://127.0.0.1:9200"

```

#### Post Kibana setup configuration <a name="kibana"></a>

1.	Define the elastic search index to look for (settings/Index name or pattern): `travel_expenses`

2.	Load the Kibana dashboards(settings/objects/Import) located at: `visualizations/kibana_travel.json`

Docker image
------------

For testing purposes one can use a preconfigured docker-compose image (visualizations/elk/docker-compose.yml):

```
version: '2'
services:
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
                 - SERVER_HOST=127.0.0.1
                depends_on:
                 - es
        logstash:
                image: logstash:5.4.2
                volumes:
                 - ../confs/:/config-dir
                command: logstash -f /config-dir/travel_expenses.conf
                ports:
                 - "5000:5000"
                depends_on:
                 - es
```

In order to start it run ([docker-compose](https://docs.docker.com/compose/install/) should be installed):

`docker-compose up`

After starting the docker-compose image, one has to follow the [Post Kibana setup configuration](#kibana)
