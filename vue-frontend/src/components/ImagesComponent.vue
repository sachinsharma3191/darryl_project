<template>
 <div>
    <div v-if="loading">
      <v-progress-circular
          indeterminate
          color="primary"
      ></v-progress-circular>
    </div>
   <div v-else>
      <div class="images">
          <v-card v-for="(image,key,index) in images" :key="index">
            <div>
              <input type="checkbox" :id="image.id" :name="image.name"
                     @change="onSelectImage(image)">
              <label :for="image.id">{{image.name}}</label>
            </div>
            <img :src="image.imageUrl" alt="image"/>
          </v-card>
        <div>
          <v-btn v-if="pageNumber > 1" elevation="2" @click="onPreviousPageHandler">Previous</v-btn>
          <v-btn elevation="2" @click="onNextPageHandler">Next</v-btn>
        </div>
        <div v-if="selectedImages">
            <li  v-for="(selectedImage,key) in selectedImages"  :key="key">
                {{selectedImage}}
            </li>
        </div>
      </div>
   </div>
 </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "Images",
  data() {
    return {
      images: [],
      imageUrl: "http://localhost:5000/image/",
      error: null,
      paginationList:[],
      pageNumber: 1,
      selectedImages: [],
      totalPages: [],
      filterPages: [],
      size: 10,
      loading: false,
    }
  },
  async mounted() {
    await this.loadTotalPages();
    await this.loadImages();
  },
  methods: {
    async loadImages() {
      this.loading = true;
      await axios.get(this.imageUrl + this.pageNumber).then(resp => {
        const images = resp.data.payload;
        console.log(resp.data);
        let transformedImages = [];
        let count = 0;
        for (let image of images) {
            const imgObject = {
              id: ++count,
              name: image.name,
              imageUrl: `data:image/png;base64,${image.image}`,
              checked: false
            };
            transformedImages.push(imgObject)
        }
        this.images = transformedImages;
        this.loading = false;
      }).catch(error => {
        let errorStatus;
        if (!error.response) {
          errorStatus = 'Error: Network Error';
        } else {
          errorStatus = error.response.data.message;
        }
        this.loading = true;
        this.error = errorStatus;
      })
    },
    async loadTotalPages() {
      await axios.get(this.imageUrl + "total_pages").then(resp => {
        this.totalPages = resp.data.total_pages;
      }).catch(error => {
        let errorStatus;
        if (!error.response) {
          errorStatus = 'Error: Network Error';
        } else {
          errorStatus = error.response.data.message;
        }
        this.error = errorStatus;
      });
    },
    async onNextPageHandler() {
      let newPage = this.pageNumber + 1;
      this.pageNumber = newPage;
      await this.loadImages();
    },
    async onPreviousPageHandler() {
      let newPage = this.pageNumber - 1;
      if (newPage < 1) {
        newPage = 1;
      }
      this.pageNumber = newPage;
      await this.loadImages();
    },
    onSelectImage: function (imgObj) {
      const selectedImage = this.images.filter(image => image.name === imgObj.name)[0];
      selectedImage.checked = !selectedImage.checked;

      if (selectedImage.checked) {
        const index = this.selectedImages.indexOf(imgObj.name);
        if (index == -1) {
          this.selectedImages.push(imgObj.name);
        }
      } else {
        const index = this.selectedImages.indexOf(imgObj.name);
        if (index > -1) {
          this.selectedImages.splice(index, 1);
        }
      }
    }
  }
}
</script>

<style scoped>

</style>