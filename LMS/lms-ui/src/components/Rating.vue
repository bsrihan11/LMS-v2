<template>
    <div class="rating">
        <div v-for="star in totalStars" :key="star" @mouseover="hoverRating(star)" @click="setRating(star)"
            @mouseleave="resetRating()" :class="{ 'filled': star <= currentRating }"
            :style="{ 'pointer-events': disabled ? 'none' : 'auto' }">
            <span class="star"><i class="fa-solid fa-star"></i></span>
        </div>
    </div>
</template>

<script>
export default {
  name: 'Rating',
  props: {
    initialRating: {
      type: Number,
      default: 0,
      validator: rating => rating >= 0 && rating <= 5
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      currentRating: this.initialRating,
      totalStars: 5
    };
  },
  methods: {
    hoverRating(rating) {
      if (!this.disabled) {
        this.currentRating = rating;
      }
    },
    resetRating() {
      if (!this.disabled) {
        this.currentRating = this.initialRating;
      }
    },
    setRating(rating) {
      if (!this.disabled) {
        this.currentRating = rating;
        // You can emit an event here to send the new rating to the parent component
        this.$emit('update:initialRating', this.currentRating);
      }
    }
  }
}
</script>

<style>
.rating {
    display: flex;
}

.star {
    font-size: 24px;
    cursor: pointer;
}

.filled {
    color: gold;
}
</style>
