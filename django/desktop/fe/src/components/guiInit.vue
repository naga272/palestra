<template>
    <div id="guiTop">
        <div v-for="(item, index) in filesystem" :key="index" class="containerIcon" @click="openObject(item)">
            <figure>
                <img 
                    :src="(item.type === 'directory')? foldericon : fileicon" 
                    alt="{{ item.name }}"
                    width="40px"
                    height="40px"
                />
                <figcaption class="nameFile">
                    {{ item.name }}
                </figcaption>
            </figure>
        </div>
        <div id="container-guiDir">
            <div id="guiDir" v-show="showGuiDir">
                Hello Wortld
            </div>
        </div>
    </div>

    <div id="bottombar">
        <div id="orarioForm"></div>
    </div>

</template>


<script>

import foldericon from "@/assets/folder.png"
import fileicon from "@/assets/file.png"


export default {
    name: "guiInit",
    props: ["username", "filesystem"],
    data() {
        return {
            foldericon,
            fileicon,
            guiFolder: false,
        }
    },
    mounted() {
        console.log(this.filesystem);
        
        const orario = document.getElementById("orarioForm");

        const getOrario = () => {
            const ora = new Date();
            const opzioni = {
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
                hour12: false
            };

            const orarioFormattato = ora.toLocaleTimeString("it-IT", opzioni);
            orario.innerHTML = orarioFormattato;
        }

        setInterval(getOrario, 1000);
        getOrario();
    },
    methods:{
        openObject(item){
            this.guiFolder = !this.guiFolder;
            console.log(item)
            if (this.guiFolder) {
                console.log("sono nel true");
            } else {
                console.log("non sono piu nel true");
            }
        }
    }
}


</script>

<style scoped>

    #guiTop{
        width: 100%;
        height: 90vh;
        display: flex;
        flex-direction: column;
    }

    .containerIcon{
        width: 70px;
        text-align: center;
        justify-content: center;
        justify-items: center;
        margin-left: 20px;
        margin-top: 20px;
    }

    .containerIcon:hover{
        cursor: pointer;
        background-color: rgba(114, 185, 248, 0.1);
        
    }

    .nameFile{
        color:#fff;
        font-size: 1.5em;
    }

    #container-guiDir{
        position: absolute;
        width: 100%;
        height: 90vh;
        margin: 0 auto;
        z-index: 100;
        text-align: center;
        justify-content: center;
        justify-items: center;
        align-items: center;
    }

    #guiDir{
        width: 50vh;
        height: 50vh;
        margin: 0 auto;
        background-color: blue;
    }

    #bottombar{
        width: 100%;
        height: 10vh;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        text-align: center;
        background-color: rgba(40, 40, 46, 0.97);
        font-size: 2em;
        color: #fff;
    }

</style>