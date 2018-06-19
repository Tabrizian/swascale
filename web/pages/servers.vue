<template>
  <div>
    <v-data-table :headers="headers" :items="servers" hide-actions class="elevation-1">
      <template slot="items" slot-scope="props">
        <td>{{ props.item.name }}</td>
        <td>{{ props.item.uid }}</td>
        <td>{{ props.item.image }}</td>
        <td>{{ props.item.flavor }}</td>
        <td>{{ props.item.region }}</td>
        <td>{{ props.item.driver }}</td>
        <td>
          <v-btn icon class="mx-0" @click="deleteItem(props.item)">
            <v-icon color="red">delete</v-icon>
          </v-btn>
        </td>
      </template>
    </v-data-table>
      <v-dialog v-model="dialog" max-width="500px">
      <v-btn slot="activator" color="primary" dark class="mb-2">New Item</v-btn>
      <v-card>
        <v-card-title>
          <span class="headline">{{ formTitle }}</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12 sm12 md12>
                <v-text-field v-model="editedItem.name" label="server name"></v-text-field>
              </v-flex>
              <v-flex xs12 sm12 md12>
                <v-text-field v-model="editedItem.image" label="server image"></v-text-field>
              </v-flex>
              <v-flex xs12 sm12 md12>
                <v-text-field v-model="editedItem.flavor" label="server flavor"></v-text-field>
              </v-flex>
              <v-flex xs12 sm12 md12>
                <v-text-field v-model="editedItem.networks" label="server networks"></v-text-field>
              </v-flex>
              <v-flex xs12 sm12 md12>
                <v-text-field v-model="editedItem.region" label="server region"></v-text-field>
              </v-flex>
              <v-flex xs12 sm12 md12>
                <v-text-field v-model="editedItem.driver" label="server driver"></v-text-field>
              </v-flex>
              <v-flex xs12 sm12 md12>
                <v-text-field v-model="editedItem.key" label="server key"></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click.native="close">Cancel</v-btn>
          <v-btn color="blue darken-1" flat @click.native="save">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    </div>
    </template>


<script>
export default {
  async asyncData ({ app }) {
    let servers = await app.$axios.$get('/api/server')
    return { servers }
  },
  data () {
    return {
      editedIndex: -1,
      dialog: false,
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
        },
        {
          text: 'Actions',
          value: 'action'
        }
      ],
      editedItem: {
        name: '',
        image: '',
        flavor: '',
        networks: '',
        region: '',
        driver: '',
        key: ''
      }
    }
  },
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
    }
  },
  methods: {
    deleteItem: async function (item) {
      let objId = item._id.$oid
      if (confirm('Are You Sure To Want To Delete ' + item.name + ' ?')) {
        let deletedServer = await this.$axios.delete('/api/server/' + objId)
        return deletedServer
      }
    },
    async save () {
      if (this.editedIndex > -1) {
        // TODO EDIT ITEM
      } else {
        try {
          let networks = this.editedItem.networks.split(' ')
          await this.$axios.post('/api/server', {
            name: this.editedItem.name,
            image: this.editedItem.image,
            flavor: this.editedItem.flavor,
            networks: networks,
            region: this.editedItem.region,
            driver: this.editedItem.driver,
            key: this.editedItem.key
          })
        } catch (e) {}
        this.close()
      }
    },
    close () {
      this.dialog = false
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      }, 300)
    }
  }
}
</script>
