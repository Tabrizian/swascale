<template>
  <div>
    <v-text-field v-model="scaleUp" label="Scale Up"></v-text-field>
    <v-text-field v-model="scaleDown" label="Scale Down"></v-text-field>
    <v-data-table
    :headers="headers"
    :items="vms"
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
  async asyncData ({ app }) {
    let servers = await app.$axios.$get('/api/server')
    return { servers }
  },
  methods: {
    addVM () {
      this.vms.push({
        _id: '',
        role: ''
      })
    },
    async save () {
      await this.$axios.post('/api/cluster', {
        vms: this.vms,
        up: this.scaleUp,
        down: this.scaleDown
      })
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
      scaleUp: '',
      scaleDown: '',
      vms: [

      ]
    }
  }
}
</script>

