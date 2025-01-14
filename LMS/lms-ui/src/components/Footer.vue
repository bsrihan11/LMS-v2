<template>
      <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <h3>MAD 1 project</h3>
                <p> A library management system web app for MAD 1 project.</p>

            </div>
        </div>
    </footer>
</template>

<script>
export default {
    name:'Footer',

}
</script>

<style>
.footer {
    background-color: #1845ad;
    color: #fff;
    padding: 40px 0;

}

.container {
    width: 80%;
    margin: 0 auto;
}

.footer-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

</style>