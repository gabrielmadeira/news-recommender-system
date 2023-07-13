<template>
  <div class="about">
    <h1>Hierarchical Graph</h1>
    <svg id="mySVG" ref="mySVG" width="100%" height="1500px"></svg>
  </div>
</template>
<script>
/* eslint-disable */
  // import { ForceSimulation, Event } from "@livereader/graphly-d3";
  // import "@livereader/graphly-d3/style.css";
  // import Hexagon from "../assets/hexagon";

  import {
    select,
    json,
    tree,
    hierarchy,
    linkHorizontal,
    zoom
  } from 'd3';

  import data from '../assets/hierarchicalData.json';

  // const tree = treemap();

  export default {
    name: "HierarchicalView",
    data() {
      return {
      }
    },
    mounted() {
      const svg = select('svg');
      const width = document.body.clientWidth;
      const height = document.body.clientHeight;

      const margin = { top: 0, right: 50, bottom: 0, left: 75};
      const innerWidth = width - margin.left - margin.right;
      const innerHeight = height - margin.top - margin.bottom;

      const treeLayout = tree().size([innerHeight, innerWidth]);

      const zoomG = svg
          .attr('width', width)
          .attr('height', height)
        .append('g');

      const g = zoomG.append('g')
          .attr('transform', `translate(${margin.left},${margin.top})`);

      function handleZoom(e) {
        select('svg g').attr('transform', e.transform);
      }

      svg.call(zoom().on('zoom', handleZoom));

      console.log(data)

      const root = hierarchy(data);
      const links = treeLayout(root).links();
      const linkPathGenerator = linkHorizontal()
        .x(d => d.y)
        .y(d => d.x);
    
      g.selectAll('path').data(links)
        .enter().append('path')
          .attr('d', linkPathGenerator);
    
      g.selectAll('text').data(root.descendants())
        .enter().append('text')
          .attr('x', d => d.y)
          .attr('y', d => d.x)
          .attr('dy', '0.32em')
          .attr('text-anchor', d => d.children ? 'middle' : 'start')
          .attr('font-size', d => 3.25 - d.depth + 'em')
          .text(d => d.data.data.id);
    },
    methods: {

    }
  };

</script>
<style>
  body {
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  margin: 0;
  overflow: hidden;
}

path {
  fill: none;
  stroke: #56c2a3;
}

text {
  text-shadow:
   -1px -1px 3px white,
   -1px  1px 3px white,
    1px -1px 3px white,
    1px  1px 3px white;
  pointer-events: none;
  font-family: 'Playfair Display', serif;
}
</style>