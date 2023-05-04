<template>
  <div class="about">
    <h1>Interactive Graph</h1>
    <svg id="mySVG" ref="mySVG" width="100%" height="1500px"></svg>
  </div>
</template>
<script>
/* eslint-disable */
  import { ForceSimulation, Event } from "@livereader/graphly-d3";
  import "@livereader/graphly-d3/style.css";
  import Hexagon from "../assets/hexagon";

  export default {
    name: "AboutView",
    data() {
      return {
        protocol: 'bolt',
        host: 'localhost',
        port: 7687,
        username: 'neo4j',
        password: '88888888',
        graph: {}
      }
    },
    mounted() {
      this.connect();
      this.renderUserGraph("U169207");
    },
    methods: {
      connect() {
        return this.$neo4j.connect(this.protocol, this.host, this.port, this.username, this.password)
            .then(driver => {
                // Update the context of your app
            })
      },
      driver() {
        // Get a driver instance
        return this.$neo4j.getDriver()
      },
      createNode(id, type, description) {
        let colors = {
          "User": "#299438",
          "News": "#afb83b",
          "Entity": "#db4035",
        };
        if(this.graph.nodes.filter(e => e.id == id).length == 0) {
          let newNode = {
            id: id,
            shape: {type: "hexagon", scale: 2,},
            payload: {title: id + "\n" + description,  color: colors[type]}
          };
          this.graph.nodes.push(newNode);
        }
      },
      createLink(source, target, label) {
        if((this.graph.links.filter(e => (((e.source.id == source && e.target.id == target) || (e.source.id == target && e.target.id == source)) && e.label == label)).length == 0)
            && (this.graph.links.filter(e => (((e.source == source && e.target == target) || (e.source == target && e.target == source)) && e.label == label)).length == 0)) {
          let newLink = {
            source: source,
            target: target,
            directed: false,
            strenght: "weak",
            label: label,
          };
          this.graph.links.push(newLink);
        }
      },
      renderUserGraph(userID) {
        // Get a session from the driver
        const session = this.$neo4j.getSession();

        // Or you can just call this.$neo4j.run(cypher, params)
        session.run("MATCH (u:User{id: $userID})-[r:READ]->(n:News)-[c:CONTENT]->(e:Entity) RETURN (u),(n),(e)", {userID: userID})
          .then(res => {
              console.log(res.records);
              this.graph = {nodes: [], links: []};
              for(let i=0; i<res.records.length; i++) {
                this.createNode(res.records[i]._fields[0].properties.id, "User", "");
                this.createNode(res.records[i]._fields[1].properties.id, "News", res.records[i]._fields[1].properties.title);
                this.createNode(res.records[i]._fields[2].properties.WDId, "Entity", res.records[i]._fields[2].properties.label);
                this.createLink(res.records[i]._fields[0].properties.id, res.records[i]._fields[1].properties.id, "READ");
                this.createLink(res.records[i]._fields[1].properties.id, res.records[i]._fields[2].properties.WDId, "CONTENT");
              }
              this.render();
          })
          .then(() => {
              session.close()
          });
      },
      render() {
        const mySVG = this.$refs.mySVG;
        const simulation = new ForceSimulation(mySVG);
        simulation.templateStore.add("hexagon", Hexagon);

        simulation.on(Event.NodeClick, (event, node) => {
          let type = node.id[0];
          console.log(node.id);
          if(type == "U") {
            this.$neo4j.run("MATCH (u:User{id: $userID})-[r:READ]->(n:News) WITH n, rand() AS rnd RETURN (n) ORDER BY rnd LIMIT 5", {userID: node.id})
              .then(res => {
                  //console.log(res.records);
                  //this.graph = {nodes: [], links: []};
                  for(let i=0; i<res.records.length; i++) {
                    this.createNode(res.records[i]._fields[0].properties.id, "News", res.records[i]._fields[0].properties.title);
                    this.createLink(node.id, res.records[i]._fields[0].properties.id, "READ");
                  }
                  simulation.render(this.graph);
              });
          }
          if(type == "N") {
            this.$neo4j.run("MATCH (n:News{id: $newsID})-[r:READ]->(u:User) WITH u, rand() AS rnd RETURN (u) ORDER BY rnd  LIMIT 5", {newsID: node.id})
              .then(res => {
                  for(let i=0; i<res.records.length; i++) {
                    this.createNode(res.records[i]._fields[0].properties.id, "User", "");
                    this.createLink(node.id, res.records[i]._fields[0].properties.id, "READ");
                  }
                  simulation.render(this.graph);
              });
            this.$neo4j.run("MATCH (n:News{id: $newsID})-[c:CONTENT]->(e:Entity) WITH e, rand() AS rnd RETURN (e) ORDER BY rnd LIMIT 5", {newsID: node.id})
              .then(res => {
                  for(let i=0; i<res.records.length; i++) {
                    this.createNode(res.records[i]._fields[0].properties.WDId, "Entity", res.records[i]._fields[0].properties.label);
                    this.createLink(node.id, res.records[i]._fields[0].properties.WDId, "CONTENT");
                  }
                  simulation.render(this.graph);
              });
          }
          if(type == "Q") {
            this.$neo4j.run("MATCH (e:Entity{WDId: $entityID})-[c:CONTENT]->(n:News) WITH n, rand() AS rnd RETURN (n) ORDER BY rnd LIMIT 5", {entityID: node.id})
              .then(res => {
                  // console.log(res.records);
                  for(let i=0; i<res.records.length; i++) {
                    this.createNode(res.records[i]._fields[0].properties.id, "News", res.records[i]._fields[0].properties.title);
                    this.createLink(node.id, res.records[i]._fields[0].properties.id, "CONTENT");
                  }
                  console.log(this.graph)
                  simulation.render(this.graph);
              });
              this.$neo4j.run("MATCH (e:Entity{WDId: $entityID})-[r:RELATED]->(e2:Entity) WITH e2, rand() AS rnd RETURN (e2) ORDER BY rnd LIMIT 5", {entityID: node.id})
              .then(res => {
                  // console.log(res.records);
                  for(let i=0; i<res.records.length; i++) {
                    this.createNode(res.records[i]._fields[0].properties.WDId, "Entity", res.records[i]._fields[0].properties.label);
                    this.createLink(node.id, res.records[i]._fields[0].properties.WDId, "RELATED");
                  }
                  simulation.render(this.graph);
              });
          }
        });

        // this.graph = {
        //   nodes: [
        //     {
        //       id: "node1",
        //       shape: {
        //         type: "hexagon",
        //         scale: 2,
        //       },
        //       // x: -150,
        //       // y: 30,
        //       payload: {
        //         title: "olar",
        //         color: "#9575cd",
        //       },
        //     },
        //     {
        //       id: "node2",
        //       shape: {
        //         type: "hexagon",
        //         scale: 1,
        //       },
        //       // x: 150,
        //       // y: -30,
        //       payload: {
        //         title: "test",
        //         color: "#111111",
        //       },
        //     },
        //   ],
        //   links: [
        //     {
        //       source: "node1",
        //       target: "node2",
        //       directed: true,
        //       strength: "weak",
        //       label: "olooko",
        //     },
        //   ],
        // };

        simulation.render(this.graph);
      }
    }
  };

</script>