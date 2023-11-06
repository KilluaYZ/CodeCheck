<template>
<!--    <el-slider v-model='font_size' :min='10' :max='50'/>-->
<el-container style='width: 100%; height: 100%'>
    <el-header id='Container-Header' style=' width: 100%; height: 40px'>
        <el-row class='header-card' align='middle' justify='space-between'>
            <el-text size='large' style='font-weight: bolder'>CodeCheck</el-text>
            <el-popover :visible="visible" placement="top" :width="300">
                <el-text size='large'>设置</el-text>
                <el-row>
                    <el-text>字体大小</el-text>
                    <el-slider v-model='font_size' :min='12' :max='50'/>
                </el-row>
                <template #reference>
                    <el-button :icon='Setting' circle ></el-button>
                </template>
            </el-popover>
        </el-row>
    </el-header>
    <el-main style='width: 100%; padding: 0;margin: 0;'>
        <el-row style='height: 100%; width: 100%'>
            <splitpanes style='height: 100%; width: 100%' >
                <pane min-size='10' size='30' style='height: 100%'>
                    <div id='Container-Aside'>
                        <el-tabs class='left_tabs' v-model='activeName' type='border-card'>
                            <el-tab-pane label='问题' name='first' >
                                <div style='height: 100%; width: 100%;'>
                                    <el-scrollbar>
                                        <el-row v-for='(problem ,index) in ProblemsList'>
                                            <ProblemCard
                                                :problem-id='problem.problemId'
                                                :file-path='problem.filePath'
                                                :problem-class-name='problem.problemClassName'
                                                :problem-detail-json-string='problem.problemDetail'
                                                :problem-severity='problem.severity'
                                                :id='index+1'
                                                :go-to-line='goToFileLineByFilePathAndLine'
                                            />
                                        </el-row>
                                    </el-scrollbar>
                                </div>
                            </el-tab-pane>
                            <el-tab-pane label='AI助手' name='second' style='height: 100%'>
                                <div style='height: 100%; width: 100%'>
                                    <el-container style='height: 100%; width: 100%'>
                                        <el-main v-loading='sendChatBtnIsDisabled' element-loading-text='正在思考，请稍等...' style='height: 100%;background-color: #fdfdfd'>
                                            <template v-for='chatItem in chatHistory'>
                                                <el-row  justify='start' :style='{width: "100%"}'>
                                                    <el-row v-if='chatItem.role === "assistant"' style='width: 100%'>
                                                        <el-avatar  :size='30' :src='AiAvatar' style='margin-right: 5px'/>
                                                        <el-card class='ChatCard' shadow='hover'>
                                                            <v-md-preview style='width: 100%' :text='chatItem.content'></v-md-preview>
                                                        </el-card>
                                                    </el-row>
                                                    <el-row v-else justify='end' style='width: 100%; '>
                                                        <el-card class='ChatCard' shadow='hover'>
                                                            <v-md-preview style='width: 100%' :text='chatItem.content'></v-md-preview>
                                                        </el-card>
                                                        <el-avatar :size='25' src='https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png' style='margin-left: 10px;'/>

                                                    </el-row>

                                                </el-row>
                                            </template>
                                        </el-main>
                                        <el-footer  style='background-color: #fdfdfd; min-height: 100px; max-height: 50%; height: fit-content'>
                                            <el-row justify='center' style='margin-bottom: 10px'>
                                                <el-button type='primary' @click='startNewChat'>+新对话</el-button>
                                            </el-row>
                                            <el-card style='height: 100%; width: 100%'>
                                                <el-row style='height: fit-content; flex-wrap: nowrap;' align='middle'>
                                                    <el-input type='textarea' :row='5' v-model='userInputText' style='margin-right: 10px;' />
                                                    <el-button circle :icon='Promotion' :disabled='sendChatBtnIsDisabled' type='primary' size='large' @click='onClickChatSendBtn'></el-button>
                                                </el-row>
                                            </el-card>
                                        </el-footer>
                                    </el-container>
                                </div>
                            </el-tab-pane>
                        </el-tabs>
                    </div>
                </pane>
                <pane style='height: 100%' min-size='10'>
                    <div id='Container-Main'>
<!--                        <DynamicScroller-->
<!--                            :items='codes'-->
<!--                            :min-item-size='14'-->
<!--                            style='height: 100%'-->
<!--                        >-->
<!--                            <template v-slot="{ item, index, active }">-->
<!--                                <DynamicScrollerItem-->
<!--                                    :item='item'-->
<!--                                    :size-dependencies='[-->
<!--                                        item.content-->
<!--                                    ]'-->
<!--                                    :active='active'-->
<!--                                    :data-index='index'-->
<!--                                >-->
<!--                                    <el-row class='code-line'>-->
<!--                                        <el-text class='code-line-number'-->
<!--                                                 :style="{-->
<!--                            fontSize: font_size + 'px',-->
<!--                            minWidth: (2*font_size) + 'px',-->
<!--                            marginRight: (Math.round(font_size / 2)) + 'px',-->
<!--                            paddingRight: (Math.round(font_size / 2)) + 'px'-->
<!--                        }">{{index}}</el-text>-->
<!--                                        <el-text class='code-line-code' :style="{fontSize: font_size + 'px'}">-->
<!--<pre>-->
<!--{{item.content}}-->
<!--</pre>-->
<!--                                        </el-text>-->
<!--                                    </el-row>-->
<!--                                </DynamicScrollerItem>-->
<!--                            </template>-->
<!--                        </DynamicScroller>-->
<!--                    <el-affix position='top' :offset='20'>-->
<!--                        -->
<!--                    </el-affix>-->

                        <el-row
                            :style='{fontSize: font_size + "px", backgroundColor: "#fdfdfd", height: (font_size + 10) + "px" }'
                            style='width: 100%'
                            align='middle'
                        >
                            <el-button class='directory_btn' :style='{fontSize: (font_size - 5) + "px"}' type='primary' text @click='backToRoot()'>/</el-button>
                            <template v-for='(path, index) in pathStack'>
                                <template v-if='path.fileCategory === "directory"'>
                                    <el-button class='directory_btn' type='primary' :style='{fontSize: (font_size - 5) + "px"}' text @click='updatePathStack(index)'>{{path.fileName}}</el-button>
                                    <el-text class='directory_btn' :style='{fontSize: (font_size - 5) + "px"}'>/</el-text>
                                </template>
                                <template v-else>
                                    <el-button class='directory_btn' type='primary' :style='{fontSize: (font_size - 5) + "px"}' :disabled='true' text @click='updatePathStack(index)'>{{path.fileName}}</el-button>
                                </template>
                            </template>
                        </el-row>

                        <template v-if='displayCode' v-for='(item, index) in codes'>
                            <template v-if='item.problem'>
                                <el-row v-for='problemItem in item.problem'>
                                    <el-card style='width: 100%; margin: 5px;'>
                                        <el-row><el-text type='danger' :style='{fontSize: font_size + "px", fontWeight: "bolder"}'>{{"问题(ID"+problemItem.problemId+")::"+problemItem.problem_class.severity}}</el-text></el-row>
                                        <el-row><el-text type='danger' :style='{fontSize: font_size + "px", fontWeight: "normal"}'>{{problemItem.description}}</el-text></el-row>
                                    </el-card>
                                </el-row>
                            </template>
                            <template v-if='item.trace'>
                                <el-row v-for='traceItem in item.trace'>
                                    <el-card style='width: 100%; margin: 5px;'>
                                        <el-row><el-text type='primary' :style='{fontSize: font_size + "px", fontWeight: "bolder"}'>{{"问题(ID"+traceItem.problemId+")路径::"+traceItem.kind}}</el-text></el-row>
                                        <el-row><el-text type='primary' :style='{fontSize: font_size + "px", fontWeight: "normal"}'>{{traceItem.desc}}</el-text></el-row>
                                    </el-card>
                                </el-row>
                            </template>

                            <el-row class='code-line' :style='{ backgroundColor: item.problem ? "#f89898" : item.trace ? "#a0cfff" : "#fdfdfd" }' :id='"code-line-"+(index + 1)'>
                                <el-text class='code-line-number'
                                         :style="{
                            fontSize: font_size + 'px',
                            minWidth: (2*font_size) + 'px',
                            marginRight: (Math.round(font_size / 2)) + 'px',
                            paddingRight: (Math.round(font_size / 2)) + 'px'
                        }">{{index+1}}</el-text>
                                    <el-text class='code-line-code' :style="{fontSize: font_size + 'px'}">
<pre>
{{item.content}}
</pre>
                                    </el-text>
                            </el-row>
                        </template>


                        <el-row v-if='displayDir' v-for='(file, index) in dirData' :style='{fontSize: font_size + "px", marginLeft: 10 + "px"}' align='middle'>
                            <template v-if='file.fileCategory === "directory"'>
                                <el-icon ><Folder /></el-icon>
                                <el-button text type='info' :style='{fontSize: font_size + "px"}'  @click='onClickDirPageFile(file.fileName, file.fileCategory)'>{{file.fileName}}</el-button>
                            </template>
                            <template v-else-if='file.fileCategory === "text"'>
                                <el-icon><Document /></el-icon>
                                <el-button text type='info' :style='{fontSize: font_size + "px"}' @click='onClickDirPageFile(file.fileName, file.fileCategory)'>{{file.fileName}}</el-button>
                            </template>
                            <template v-else>
                                <el-icon><DocumentDelete /></el-icon>
                                <el-button text :disabled='true' type='info' :style='{fontSize: font_size + "px"}' @click='onClickDirPageFile(file.fileName, file.fileCategory)'>{{file.fileName}}</el-button>
                            </template>
                        </el-row>
                    </div>
                </pane>
            </splitpanes>
        </el-row>
    </el-main>
</el-container>


</template>

<script setup lang='ts'>
import { useRoute } from 'vue-router'
import request from '@/utils/request'
import { getFile } from '@/api/file'
import { onMounted, reactive, ref, toRef } from 'vue'
import type Node from 'element-plus/es/components/tree/src/model/node'
import { Storage } from '@/utils/cache'
import { getProjectProblems } from '@/api/project'
import { Delete, Discount, Setting, Promotion } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import chatAi from '@/api/ai'
import { types } from 'sass'
import List = types.List
import AiAvatar from '@/assets/images/AiAvatar.jpg'

const codes = ref([])
const route = useRoute();
var projectId = route.query.projectId;
const language = ref('')
const font_size = ref(18)
const activeName = ref('first')
const displayCode = ref(false)
const displayDir = ref(false)
const pathStack = ref([
    // {
    //     "fileCategory": "directory",
    //     "fileName": "arm"
    // },
    // {
    //     "fileCategory": "directory",
    //     "fileName": "sss"
    // },
    // {
    //     "fileCategory": "file",
    //     "fileName": "1.c"
    // }
])

const dirData = ref([])
const selected_text = ref("")
const sendChatBtnIsDisabled = ref(false)
window.addEventListener("mouseup", (e) => {
    selected_text.value = window.getSelection().toString();
})

const userInputText = ref("")
const chatHistory = ref([])

const pushPath = (fileCategory: string, fileName: string) => {
    pathStack.value.push({
        fileCategory: fileCategory,
        fileName: fileName
    })
}

const clearPathStack = () => {
    pathStack.value = [];
}

const backToRoot = () => {
    clearPathStack();
    return goToDirOrFile();
}
const popPath = () => {
    return pathStack.value.pop()
}

const goToDirOrFile = () => {
    let currentPathInfo = getFilePathByStack();
    Storage.setItem(projectId+"-pathInfo", {
        filePath: currentPathInfo.filePath,
        fileName: currentPathInfo.fileName,
        fileCategory: currentPathInfo.fileCategory
    })
    return getInfo(currentPathInfo.filePath, currentPathInfo.fileName);
}
//var fruits = ["Banana", "Orange", "Lemon", "Apple", "Mango"];
//var citrus = fruits.slice(1,3);
//Orange,Lemon
const updatePathStack = (idx: number) => {
    pathStack.value = pathStack.value.slice(0, idx+1)
    // console.log(getFilePathByStack())
    return goToDirOrFile();
}

const getFilePathByStack = () => {
    if(pathStack.value.length === 0){
        return {
            filePath: "/",
            fileName: "",
            fileCategory: "directory"
        }
    }

    let filePath = "/";
    pathStack.value.forEach(item => {
        filePath += item.fileName + "/";
    })
    if(pathStack.value.length > 0){
        filePath = filePath.substring(0,filePath.length - 1);
    }

    let idx = filePath.lastIndexOf("/")
    let fileRootPath = filePath.substring(0, idx);
    let fileName = filePath.substring(idx+1)
    let fileCategory = pathStack.value[pathStack.value.length - 1].fileCategory;
    return {
        filePath: fileRootPath,
        fileName: fileName,
        fileCategory: fileCategory
    };
}

const getInfo = (filePath: string, fileName: string) => {
    // getFile("23", "/", "pngtest.c").then((res) => {
    //     codes.value = res.data.content;
    //     language.value = res.data.fileType;
    // })

    return new Promise((resolve, reject) => {
        getFile(projectId, filePath, fileName).then((res) => {
            let fileCategory = res.data.fileCategory;
            let fileContent = res.data.content;
            if(fileCategory === 'directory'){
                displayDir.value = true;
                displayCode.value = false;
                dirData.value = fileContent.children;
            }else if(fileCategory === 'text'){
                displayCode.value = true;
                displayDir.value = false;
                codes.value = fileContent;
                console.log(fileContent)
            }else{
                displayCode.value = false;
                displayDir.value = false;
            }
            resolve("success");
        })
    })
}

const onClickDirPageFile = (fileName: string, fileCategory: string) => {
    pushPath(fileCategory, fileName);
    // let currentPathInfo = getFilePathByStack();
    // getInfo(currentPathInfo.filePath, currentPathInfo.fileName);
    return goToDirOrFile();
}

const initInfo = () => {
    getProblemInfo();
    let pathInfo = Storage.getItem(projectId + "-pathInfo");
    if(pathInfo === undefined || pathInfo === null){
        getInfo("/","");
        return;
    }

    let filePath = pathInfo.filePath;
    let fileName = pathInfo.fileName;
    let fileCategory = pathInfo.fileCategory;
    if(filePath === undefined || filePath === null || fileName === undefined || fileName === null || fileCategory === undefined || fileCategory === null){
        getInfo("/","");
    }else{
        goToDirOrFileByFilePathAndFileName(filePath, fileName, fileCategory);
    }
    // goToDirOrFileByFilePathAndFileName("/arm","arm_init.c");

}

const goToDirOrFileByFilePathAndFileName = (filePath: string, fileName: string, fileCategory: string) => {
    clearPathStack();
    console.log("fileName: "+fileName)
    console.log("filePath: "+filePath)
    console.log("fileCategory: "+fileCategory)
    let filePathList = filePath.split("/");
    let processedFilePathList = [];
    filePathList.forEach(item => {
        if(item !== ""){
            processedFilePathList.push(item);
        }
    });
    processedFilePathList.forEach(item => {
        pushPath("directory", item)
    });
    if(fileName !== ""){
        pushPath(fileCategory, fileName);
    }
    return goToDirOrFile();
}
const ProblemsList = ref([])
const getProblemInfo = () => {
    getProjectProblems(projectId).then(res => {
        ProblemsList.value = res.data;
    })
}

const goToLine = (line: number) => {
    let line_id = "code-line-"+line;
    document.getElementById(line_id)?.scrollIntoView();
}

const goToFileLineByFilePathFileNameLine = (filePath: string, fileName: string, line: number) => {
    goToDirOrFileByFilePathAndFileName(filePath, fileName, "text").then((res) => {
        goToLine(line);
    })
}

const goToFileLineByFilePathAndLine = (fileRelativePath: string, line: number) => {
    console.log("enter function")
    let idx = fileRelativePath.lastIndexOf("/");
    let filePath = fileRelativePath.substring(0,idx);
    let fileName = fileRelativePath.substring(idx+1,);
    goToFileLineByFilePathFileNameLine(filePath, fileName, line);
}

const onClickChatSendBtn = () => {
    if(userInputText.value === null || userInputText.value === undefined || userInputText.value === ""){
        ElMessage({
            type: "warning",
            message: "请在聊天框内输入内容"
        })
        return;
    }
    sendChatBtnIsDisabled.value = true;
    chatHistory.value.push({
        "role":"user",
        "content": userInputText.value
    })
    userInputText.value = "";
    chatAiUpdateChatHistory(chatHistory.value)
}

const loadChatHistoryFromStorage = () => {
    let chat_history = Storage.getItem(projectId + "-chat-history");
    if(chat_history === undefined || chat_history === null){
        return null;
    }
    return chat_history;
}

const chatAiUpdateChatHistory = (chat_history: List) => {
    chatAi(chat_history).then(res => {
        let reply = res.data.reply;
        chatHistory.value.push({
            "role": "assistant",
            "content": reply
        })
        Storage.setItem(projectId + "-chat-history", chatHistory.value);
        sendChatBtnIsDisabled.value = false;
    })
}

const initChatHistory = () => {
    let chat_histroy = loadChatHistoryFromStorage();
    if(chat_histroy === null){
        console.log("本地没有存储chatHistory")
        chat_histroy = [{
            "role":"user",
            "content":"你好！"
        }]
        chatHistory.value = chat_histroy;
        chatAiUpdateChatHistory(chat_histroy)
    }else{
        chatHistory.value = chat_histroy;
    }
}

const startNewChat = () => {
    let chat_histroy = [{
        "role":"user",
        "content":"你好！"
    }]
    chatHistory.value = chat_histroy;
    chatAiUpdateChatHistory(chat_histroy)
}

onMounted(initInfo)
onMounted(initChatHistory)
// onMounted(updateWidth)
</script>

<style scoped lang='scss'>

html, body, #app{
    width: 100vw;
    height: 100vh;
    overflow: hidden;
}

.code-line{
    background-color: #fdfdfd;
}

.code-line-number{
    color: #989898;
    background-color: #e8e8e8;
    text-align: end;
    user-select: none;
}

.code-line-code{
    color: #303133;

}

#Container-Header{
    background-color: #fdfdfd;
    box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.09);
    margin: 1px 1px 1px 1px;
    padding-left: 30px;
    padding-right: 30px;
}

#Container-Header .header-card{
    width: 100%;
    height: 100%;
}


#Container-Aside{
    background-color: #fdfdfd;
    height: 100%;
    width: 100%;
    //overflow-x: scroll;
    overflow-y: scroll;
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none; /* IE 10+ */

}

::-webkit-scrollbar {
    display: none; /* Chrome Safari */
}

#Container-Main{
    background-color: #eaf3fd;
    height: 100%;
    width: 100%;
    //overflow-x: scroll;
    overflow-y: auto;
}

#drag_divider{
    height: 100%;
    width: 5px;
    background-color: #337dcb;
}

#drag_divider:hover{
    background-color: #6e6775;
}


.span-devider{
    background-color: #337ecc;
    width: 10px;
}

.directory_btn{
    padding: 5px;
    margin: 0 5px 0 5px;
    font-weight: bolder;
}

.left_tabs{
    height: 100%;
    width: 100%;
}

//.ChatCard {
//    padding: 0;
//    margin: 0;
//    .el-card__body {
//        padding: 0;
//    }
//}

.ChatCard{
    width: fit-content;
    max-width: 90%;
    padding: 0;
    margin-bottom: 10px;
    border-radius: 12px;
}

@import "splitpanes/dist/splitpanes.css";
</style>