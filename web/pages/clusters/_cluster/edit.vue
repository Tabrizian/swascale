<template>
  <div>
    <v-text-field label="Scale Up" v-model="cluster.up"></v-text-field>
    <v-text-field label="Scale Down" v-model="cluster.down"></v-text-field>
    <v-data-table
    :headers="headers"
    :items="cluster.vms"
    hide-actions
    class="elevation-1"
  >
    <template slot="items" slot-scope="props">
      <td><v-select
          :items="servers"
          v-model="props.item._id"
          label="Select Server"
          item-value="_id.$oid"
          item-text="name"
          single-line
        ></v-select></td>
      <td><v-select
          :items="roles"
          v-model="props.item.role"
          label="Select Role"
          single-line
        ></v-select></td>
    </template>
  </v-data-table>
  <v-btn color="primary" @click.native="addVM">Add VM</v-btn>
  <v-btn color="success" @click.native="save">Save</v-btn>
  </div>
</template>
<script>
export default {
  async asyncData ({ app, params }) {
    let servers = await app.$axios.$get('/api/server')
    let cluster = await app.$axios.$get('/api/cluster/' + params.cluster)
    return { servers, cluster }
  },
  methods: {
    addVM () {
      this.cluster.vms.push({
        _id: '',
        role: ''
      })
    },
    async save () {
      await this.$axios.post('/api/cluster/' + this.cluster._id.$oid, this.cluster)
    }
  },
  data () {
    return {
      headers: [
        {
          text: 'VM Name',
          value: 'name'
        },
        {
          text: 'Role',
          value: 'role'
        }
      ],
      roles: [
        'manager',
        'worker'
      ],
      cluster: {
        up: '',
        down: '',
        vms: [

        ]
      }
    }
  }
}
</script>

