<template>
  <div ref="map" class="map" id="viewDiv">
  </div>
</template>


<script>
    import {
        loadModules
    } from 'esri-loader';

    export default {
        name: 'Map',
        mounted() {
            // lazy load the required ArcGIS API for JavaScript modules and CSS
            loadModules(['esri/Map', 'esri/views/MapView'], {css: true})
                .then(([ArcGISMap, MapView]) => {
                    const map = new ArcGISMap({
                        basemap: 'topo-vector'
                    });

                    this.view = new MapView({
                        container: this.$el,
                        map: map,
                        center: [-118, 34],
                        zoom: 8
                    });
                });
        },
        beforeDestroy() {
            if (this.view) {
                // destroy the map view
                this.view.container = null;
            }
        }
    };

    // export default {
    //     name: 'Map',
    //     mounted() {
    //         // this.loadMap([-56.049, 38.485]);
    //         this.loadMap([20.593684, 78.96288]);
    //     },
    //     methods: {
    //         loadMap(posi) {
    //             var position = posi;
    //             loadModules(['esri/map'])
    //                 .then(([Map]) => {
    //                     // create map with the given options
    //                     const map = new Map(this.$refs.map, {
    //                         // center:  [28.394857,84.124008],
    //                         center: position,
    //                         zoom: 5,
    //                         basemap: 'gray',
    //                     })
    //                         .catch(err => {
    //                             // handle any script or module loading errors
    //                             console.error(err);
    //                         });
    //                 });
    //         }
    //     }
    // }
</script>

<style scoped>
  @import url('https://js.arcgis.com/3.23/esri/css/esri.css');
  @import url('https://js.arcgis.com/3.23/esri/Map.js');
  @import url('https://js.arcgis.com/3.23/esri/views/MapView.js');

  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }

  #nav {
    padding: 30px;
  }

  #nav a {
    font-weight: bold;
    color: #2c3e50;
  }

  #nav a.router-link-exact-active {
    color: #42b983;
  }

  #viewDiv {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
  }

</style>
