<template>
  <v-layout>
    <v-flex xs12 sm6 >
      <v-card>
        <v-card-media src="https://zdnet1.cbsistatic.com/hub/i/r/2016/09/15/ca093da9-b3c5-4487-afeb-338034e946b8/resize/770xauto/838566b499a97b2cd414d36616260683/serverroom.jpg" height="400px">
        </v-card-media>
        <v-card-title primary-title>
          <div>
            <h3 class="headline mb-0">{{ numberOfServers }} servers created</h3>
          </div>
        </v-card-title>
        <v-card-actions>
          <v-btn color="primary" to='/servers'>See all</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
    <v-flex xs12 sm6 offset-sm1>
      <v-card>
        <v-card-media src="http://en.proft.me/media/science/r_kmean.png" height="400px">
        </v-card-media>
        <v-card-title primary-title>
          <div>
            <h3 class="headline mb-0">{{ numberOfClusters }} clusters defined</h3>
          </div>
        </v-card-title>
        <v-card-actions>
          <v-btn color="primary" to='/clusters'>See all</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>
<script>
export default {
  computed: {
    numberOfServers: function () {
      console.log(this.servers)
      return this.servers.length
    },
    numberOfClusters: function () {
      console.log(this.clusters)
      return this.clusters.length
    }
  },
  async asyncData ({app}) {
    let servers = {}
    let clusters = {}
    try {
      servers = await app.$axios.$get('/api/server')
      clusters = await app.$axios.$get('/api/cluster')
      console.log(servers)
      console.log(clusters)
    } catch (e) {
      console.log(e)
    }
    return {servers, clusters}
  }
}
</script>
