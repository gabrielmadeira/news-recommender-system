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
    name: "TestGraphlyView",
    data() {
      return {
        graph: { nodes: [], links: [] },
        nNodes: 44
      }
    },
    mounted() {
      this.render();
    },
    methods: {
      createNode(id, description) {
        if(this.graph.nodes.filter(e => e.id == id).length == 0) {
          let newNode = {
            id: id,
            shape: {type: "hexagon", scale: 2,},
            payload: {title: id,  color: "#299438"}
          };
          if(id == "0") {
            newNode.anchor = {
              type: 'hard',
              x: 0,
              y: 0
            }
          }
          this.graph.nodes.push(newNode);
        }
      },
      createLink(source, target, label) {
        if((this.graph.links.filter(e => (((e.source.id == source && e.target.id == target) || (e.source.id == target && e.target.id == source)) && e.label == label)).length == 0)
            && (this.graph.links.filter(e => (((e.source == source && e.target == target) || (e.source == target && e.target == source)) && e.label == label)).length == 0)) {
          let newLink = {
            source: source,
            target: target,
            directed: true,
            strenght: "strong",
            label: label,
          };
          this.graph.links.push(newLink);
        }
      },
      render() {
        const mySVG = this.$refs.mySVG;
        const simulation = new ForceSimulation(mySVG);
        simulation.templateStore.add("hexagon", Hexagon);

        this.createNode("0", "0");
        for(let i=1; i<this.nNodes; i++) {
          this.createNode(i.toString(), i.toString());
          this.createLink(i.toString(), "0", "")
          // this.createLink(i.toString(), Math.floor(i/3).toString(), "")
        }

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
        //       // label: "olooko",
        //     },
        //   ],
        // };

        simulation.render(this.graph, 10);
        // simulation.moveTo({
        //   transform: { k: 0.35, x: 0, y: 0 }
        // })
      }
    }
  };

</script>