<template>
  <v-app dark>
    <v-navigation-drawer
      persistent
      temporary
      :clipped="clipped"
      app
      v-model="drawer">
      <v-list>
        <v-list-tile v-for='navItem in navItems'
          :key='navItem.id'
          :to='navItem.link'
          :href='navItem.href'>
          <v-list-tile-action>
            <v-icon>{{ navItem.icon }}</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>{{ navItem.title }}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar app fixed>
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
      <v-toolbar-title>
        <span class="white--text">swascale</span>
        <!-- <img src="/logo.jpg" height="30px"> -->
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-content>
    <v-container fluid>
      <nuxt />
    </v-container>
    </v-content>
    <v-footer height="auto">
      <span class="caption white--text">&copy; Iman Tabrizian 2018</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  mounted () {
  },
  data () {
    return {
      drawer: false,
      clipped: true,
      navItems: [
        {
          id: 1,
          title: 'Home',
          icon: 'home',
          link: '/'
        },
        {
          id: 2,
          title: 'Servers',
          icon: 'view_agenda',
          link: '/servers'
        },
        {
          id: 3,
          title: 'Clusters',
          icon: 'group_work',
          link: '/clusters'
        }
      ]
    }
  }
}
</script>
