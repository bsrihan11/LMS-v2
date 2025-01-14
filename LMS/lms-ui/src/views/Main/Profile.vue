<template>
  <section v-if="loading" class="p1" style="display:flex;flex-direction:column;align-items:center;height:fit-content;">
    <h1>Loading...</h1>
    <div class="spinner"></div>
  </section>

  <section v-else-if="logged" class="p1" style="display:flex;flex-direction:column;align-items:center;height:fit-content;">
    <div class="profile">
      <h1>User Profile</h1>
      <table>
        <tbody>
          <tr>
            <td>Name:</td>
            <td class="separator"></td>
            <td>{{ user.first_name }} {{ user.last_name }}</td>
          </tr>
          <tr>
            <td>Email:</td>
            <td class="separator"></td>
            <td>{{ user.email }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <button class="edit-btn" @click="$router.push('/auth/update-user')"><p>Edit </p><i class="fas fa-edit"></i></button>
    <div style="margin:20px auto;font-size:60px;">Your Collection</div>
    <CollectionCard v-for="(book,index) in collection" :key="index" :book='book' :id="index"></CollectionCard>
  </section>
  
  <div v-else class="p1">
    <h1 style='font-size:40px;padding-top:30px;text-align:center;'>
      Please login first
    </h1>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import CollectionCard from '@/components/CollectionCard.vue'

export default {
  name: "Profile",
  components: { CollectionCard },
  data() {
    return {
      loading: true 
    };
  },
  methods: {
    ...mapActions('auth', ['displayFlashedMessage']),
    fetchData() {

      setTimeout(() => {
        this.loading = false;
      }, 1000);
    }
  },
  computed: {
    ...mapState('auth', ['logged', 'user', 'collection'])
  },
  created() {
    this.fetchData();
  }
}
</script>

<style>
.profile {
  padding: 15px 60px;
  width: 80%;
  display: flex;
  align-items: center;
}

.profile h1 {
  font-size: 30px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

td {
  padding: 10px;
  border-bottom: 1px solid #ccc;
}

.separator {
  width: 10px;
}

table tbody tr td:nth-child(1) {
  text-align: end;
}

table tbody tr td:nth-child(3) {
  text-align: start;
}

.edit-btn {
  color: #fff;
  width:fit-content;
  background: #ad8018;
  display: flex;
  font-size: 25px;
  border: none;
  padding: 5px;
  border-radius: 10px;
  margin-top:5px;
  margin-bottom: 10px;
  cursor: pointer;
}
.edit-btn i{
  margin-left: 5px;
}
</style>
