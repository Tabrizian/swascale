<template>
<div>

    <v-data-table :headers="headers" :items="clusters" hide-actions class="elevation-1">
      <template slot="items" slot-scope="props">
        <td>{{ props.item._id.$oid }}</td>
        <td>{{ props.item.vms.length }}</td>
        <td>
          <v-btn icon class="mx-0" @click="deleteItem(props.item)">
            <v-icon color="red">delete</v-icon>
          </v-btn>
          <v-btn icon class="mx-0" :to="'/clusters/' + props.item._id.$oid + '/edit'">
            <v-icon color="yellow">edit</v-icon>
          </v-btn>
        </td>
      </template>
    </v-data-table>
    <v-btn color="primary" to="/clusters/create">New Cluster</v-btn>
</div>

</template>

<script>
export default {
  async asyncData ({ app }) {
    let clusters = await app.$axios.$get('/api/cluster')
    return { clusters }
  },
  data () {
    return {
      editedIndex: -1,
      dialog: false,
      headers: [
        {
          text: 'ID',
          value: '_id'
        },
        {
          text: 'Number of Nodes',
          value: 'nodes'
        },
        {
          text: 'Actions',
          value: 'action'
        }
      ]
    }
  },
  methods: {
    deleteItem: async function (item) {
      let objId = item._id.$oid
      if (confirm('Are You Sure To Want To Delete ' + item._id.$oid + ' ?')) {
        let deletedCluster = await this.$axios.delete('/api/cluster/' + objId)
        return deletedCluster
      }
    }
  }
}
</script>

