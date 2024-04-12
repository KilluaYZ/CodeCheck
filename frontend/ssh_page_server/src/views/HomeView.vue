<script setup lang="ts">
import { onMounted, ref } from 'vue'
import 'xterm/css/xterm.css'
import 'xterm/lib/xterm.js'
import { Terminal } from 'xterm'
// xterm.js的插件，使终端的尺寸适合包含元素。
import { FitAddon } from 'xterm-addon-fit'
// xterm.js的附加组件，用于附加到Web Socket
import { AttachAddon } from 'xterm-addon-attach'

const xterm = ref()

const initTerm = () => {
  const term = new Terminal({
    fontSize: 14,
    cursorBlink: true, //光标闪烁
    theme: {
      foreground: '#FABD2F', //字体
      background: '#293c4b' //背景色
    }
  })
  const socket = new WebSocket('ws://localhost:49411/ws')
  const attachAddon = new AttachAddon(socket)
  const fitAddon = new FitAddon()
  term.loadAddon(attachAddon)
  term.loadAddon(fitAddon)
  term.open(xterm.value)
  fitAddon.fit()
  term.focus()
}
onMounted(() => {
  initTerm()
})
</script>

<template>
  <main>
    <div ref="xterm" class="xterm"></div>
  </main>
</template>
<style>
.xterm {
  width: 700px;
  height: 500px;
  border: 1px solid #ccc;
}
</style>
