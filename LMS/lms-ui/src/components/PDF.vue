<template>
  <div class="pdf-container">
    <main>
      <h3 v-if="message">{{ message }}</h3>
      <canvas class="pdf-viewer" ref="pdfViewer"></canvas>
    </main>
    <footer>
      <ul>
        <li class="back-profile">
          <button @click="$router.push('/profile')">Back</button>
        </li>
        <li class="pagination">
  
          <button @click="goToPreviousPage" :disabled="currentPDF.currentPage <= 1">
            <i class="fas fa-arrow-alt-circle-left"></i>
          </button>
          <span class="page-info"> page {{ currentPDF.currentPage }} of {{ currentPDF.countOfPages }}</span>
          <button @click="goToNextPage" :disabled="currentPDF.currentPage >= currentPDF.countOfPages">
            <i class="fas fa-arrow-alt-circle-right"></i>
          </button>
        </li>
        <li class="zoom-control">
          <button @click="zoomIn" :disabled="currentPDF.zoom >= 2.0">+</button>
          <button @click="zoomOut" :disabled="currentPDF.zoom <= 0.5">-</button>
          <h5 style="font-size:21px;color:#fff;">Zoom: </h5>
          <span class="zoom-value">{{ currentPDF.zoom * 100 }}%</span>
        </li>
      </ul>
    </footer>
  </div>
</template>


<script>
import { mapActions, mapState } from 'vuex';
export default {
  data() {
    return {
      currentPDF: {
        file: null,
        countOfPages: 0,
        currentPage: 1,
        zoom: 1.5,
        lineNum: 0
      },
      renderTask: false,
      message: ''
    };
  },
  methods: {
    ...mapActions('auth', ['getToken']),
    zoomIn() {
      if (this.currentPDF.zoom < 2.0) { // Max zoom is 200%
        this.currentPDF.zoom = Math.min(this.currentPDF.zoom + 0.25, 2.0);
        this.renderCurrentPage();
      }
    },
    zoomOut() {
      if (this.currentPDF.zoom > 0.5) { // Min zoom is 50%
        this.currentPDF.zoom = Math.max(this.currentPDF.zoom - 0.25, 0.5);
        this.renderCurrentPage();
      }
    },
    goToNextPage() {
      if (this.currentPDF.currentPage < this.currentPDF.countOfPages) {
        this.currentPDF.currentPage += 1;
        this.renderCurrentPage();
      }
    },
    goToPreviousPage() {
      if (this.currentPDF.currentPage > 1) {
        this.currentPDF.currentPage -= 1;
        this.renderCurrentPage();
      }
    },
    async loadPDF(book_id) {
      try {
        const csrf_access_token = await this.$store.dispatch('auth/getToken');
        if (csrf_access_token) {
          const response = await fetch(`http://localhost:5000/api/pdf/${book_id}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRF-TOKEN': csrf_access_token
            },
            credentials: 'include'
          });

          if (response.ok) {
            const pdf = await response.blob();
            var blobUrl = URL.createObjectURL(pdf);
            pdfjsLib.getDocument(blobUrl).promise.then((doc) => {
              this.resetCurrentPDF();
              this.currentPDF.file = doc;
              this.currentPDF.countOfPages = doc.numPages;
              this.$refs.pdfViewer.classList.remove('hidden');

              this.renderCurrentPage();
            }).catch((error) => {
              console.error('Error loading PDF:', error);
              this.type = 'error';
              this.message = 'Loading PDF failed.'
            });
          }
          else if (response.status === 401 || response.status === 404) {
            const data = await response.json()
            this.message = data.errors.general
          }
          else {
            this.$router.replace('/error')
            this.message = 'Loading PDF failed.'
          }
        } else {
          this.$router.replace('/profile')
        }
      } catch (error) {
        console.error('Error loading PDF:', error)
        this.message = 'Loading PDF failed.'

      }
    },
    renderCurrentPage() {
      const canvas = this.$refs.pdfViewer;
      const currentPage = this.currentPDF.currentPage;
      const zoom = this.currentPDF.zoom;

      this.currentPDF.file.getPage(currentPage).then((page) => {
        const context = canvas.getContext('2d');
        const viewport = page.getViewport({ scale: zoom });
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        const renderContext = {
          canvasContext: context,
          viewport: viewport,
        };

        return page.render(renderContext).promise;
      }).catch((error) => {
        console.error('Error rendering page:', error);
      });
    },


    resetCurrentPDF() {
      this.currentPDF = {
        file: null,
        countOfPages: 0,
        currentPage: 1,
        zoom: 1.5,
      };
    },
  },
  computed: {
    ...mapState('auth', ['logged'])
  },
  async created() {

    this.loadPDF(this.$route.params.book_id)
  },
  watch: {
    $route(to, from) {
      if (to.params.book_id !== from.params.book_id) {
        this.loadPDF(to.params.book_id);
      }
    }
  }
};
</script>

<style scoped>
.pdf-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: fit-content;
  min-height: 100vh;
  background: whitesmoke;
}

main {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

h3 {
  font-size: 24px;
  background-color: #f8d7da;
  color: #721c24;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
  margin-top: 20px;
}

.pdf-viewer {
  border: 2px solid #ccc;
  border-radius: 10px;
  margin-top: 20px;
}

footer {
  background-color: #1e57da;
  padding: 10px 0;
  width: 100%;
  position: fixed;
  bottom: 0;
  left: 0;
}

ul {
  list-style-type: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 80%;
  margin: 0 auto;
}

li {
  width: fit-content;
}




.zoom-control {
  display: flex;
  align-items: center;
}

.zoom-control button {
  cursor: pointer;
  padding: 5px 10px;
  margin: 0 5px;
  font-size: 21px;
  border-radius: 5px;
  color: #fff;
  background-color: #ad8018;
  border: none;
  width: 40px
}

.zoom-value {
  font-size: 21px;
  margin-left: 10px;
  color: #fff;
}

.pagination button {
  cursor: pointer;
  padding: 5px 10px;
  margin: 0 5px;
  font-size: 21px;
  border-radius: 5px;
  color: #fff;
  background-color: #ad8018;
  border: none;
  width: 40px
}


.back-profile button {
  cursor: pointer;
  padding: 5px 10px;
  margin: 0 5px;
  font-size: 21px;
  border-radius: 5px;
  color:#fff;
  background-color: #ad8018;
  border: none;
}

.page-info {
  font-size: 21px;
  color: #fff;
  margin: 0 5px;
}

.zoom-control {
  display: flex;
  align-items: center;
}

.zoom-label {
  font-size: 18px;
  margin-right: 10px;
}

.zoom-value {
  font-size: 18px;
}
</style>