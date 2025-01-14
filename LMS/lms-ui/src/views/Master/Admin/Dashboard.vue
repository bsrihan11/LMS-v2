<template>
  <div v-if="chartData" class="dashboard">
    <div class="summary-section">
      <div class="summary-item">
        <div class="summary-label">No. of transactions in last 24hrs:</div>
        <div class="summary-value">{{ trans_24 }}</div>
      </div>
      <div class="summary-item">
        <div class="summary-label">Mean rating for books:</div>
        <div class="summary-value">{{ avg_rating }}</div>
      </div>
    </div>
    <div class="chart-section">
      <div class="chartBox">
        <Pie :data="chartData" :options="options" />
      </div>
      <div class="top-authors">
        <h2>Top Authors</h2>
        <ol>
          <li v-for="(author, index) in top_authors" :key="index">{{ author }}</li>
        </ol>
      </div>
    </div>
  </div>
  <div v-else class="loading">
    Loading...
  </div>
</template>

<script>
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend, Colors } from 'chart.js'
import { mapState } from 'vuex'
ChartJS.register(ArcElement, Tooltip, Legend, Colors)
export default {
  name: 'Dashboard',
  components: {
    Pie
  },
  computed: {
    ...mapState('master', ['admin'])
  },
  data() {
    return {
      options: {
        responsive: true,
        maintainAspectRatio: false
      },
      chartData: null,
      top_authors: null,
      trans_24: null,
      avg_rating: null
    }
  },
  watch: {
    admin(newVal) {
      if (newVal) {
        this.top_authors = newVal.top_authors
        this.trans_24 = newVal.trans_24;
        this.avg_rating = newVal.avg_rating;
        this.chartData = {
          labels: Object.keys(newVal.section_data),
          datasets: [
            {
              data: Object.values(newVal.section_data)
            }
          ]
        }

      }
      else {
        this.chartData = null;
        this.top_authors = null;
        this.trans_24 = null;
        this.avg_rating = null;
      }
    }
  },
  async created() {
    if (this.admin) {
      this.top_authors = this.admin.top_authors
      this.trans_24 = this.admin.trans_24;
      this.avg_rating = this.admin.avg_rating;
      this.chartData = {
        labels: Object.keys(this.admin.section_data),
        datasets: [
          {
            data: Object.values(this.admin.section_data)
          }
        ]
      }
    }
  }
}
</script>

<style scoped>
.chartBox {
  height: 70%;
  width: 50%;
}

.dashboard {
  padding: 20px;
  background: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 30px;
  margin:30px 20px;
}

.summary-section {
  display: flex;
  justify-content: space-around;
  margin-bottom: 30px;
  align-items: center;

}

.summary-item {
  text-align: center;
}

.summary-label {
  font-weight: bold;
  color: #333;
}

.summary-value {
  margin-top: 5px;
  font-size: 1.2em;
  color: #555;
}

.chart-section {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  align-items: center;
}

.top-authors {
  margin-left: 30px;
}

.top-authors h2 {
  font-size: 1.5em;
  margin-bottom: 10px;
  color: #333;
}

.top-authors ol {
  padding-left: 0;
}

.top-authors li {
  margin-bottom: 5px;
  color: #555;
  margin-left:20px;
}

</style>
