<template>
  <v-data-table :headers="headers" :items="servers" hide-actions class="elevation-1">
        <template slot="items" slot-scope="props">
          <td>{{ props.item.name }}</td>
          <td>{{ props.item.uid }}</td>
          <td>{{ props.item.image }}</td>
          <td>{{ props.item.flavor }}</td>
          <td>{{ props.item.region }}</td>
          <td>{{ props.item.driver }}</td>
        </template>
  </v-data-table>
</template>

<script>
export default {
  async asyncData ({ app }) {
    let servers = await app.$axios.$get('/api/server')
    return { servers }
  },
  data () {
    return {
      headers: [
        {
          text: 'Name',
          value: 'name'
        },
        {
          text: 'Universal ID',
          value: 'uid'
        },
        {
          text: 'Image Name',
          value: 'image'
        },
        {
          text: 'Flavor',
          value: 'flavor'
        },
        {
          text: 'Region',
          value: 'region'
        },
        {
          text: 'Driver',
          value: 'driver'
        }
      ]
    }
  }
}
</script>
