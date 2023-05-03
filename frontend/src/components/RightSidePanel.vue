<template>
  <el-card class="leaflet-container" :body-style="{ padding: '0px' }" shadow="hover">
    <div id="ip">IP: {{ clientInfo.geoplugin_request }}</div>
    <div id="map"></div>
  </el-card>
  <el-card class="chart-container" :body-style="{ padding: '0px' }" shadow="hover">
    <v-chart class="chart" :option="option" autoresize />
  </el-card>
</template>

<script lang="ts" setup>
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { API } from '@/request'
import { use } from 'echarts/core'
import VChart from 'vue-echarts'
import { BarChart } from 'echarts/charts'
import { LabelLayout, UniversalTransition } from 'echarts/features'
import { CanvasRenderer } from 'echarts/renderers'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent
} from 'echarts/components'

use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent,
  BarChart,
  LabelLayout,
  UniversalTransition,
  CanvasRenderer
])

const map = ref('')
const clientInfo: any = ref({})

const siteData = ref({
  articleCnt: 0,
  userCnt: 0
})

onMounted(() => {
  axios.get('http://www.geoplugin.net/json.gp').then((res) => {
    clientInfo.value = res.data
    initMap()
  })
  API.index('/getSiteData').then((resp) => {
    siteData.value = resp.data
    option.value.series[0].data = [siteData.value.articleCnt, siteData.value.userCnt]
  })
})

const initMap = () => {
  map.value = L.map('map', {
    center: [clientInfo.value.geoplugin_latitude, clientInfo.value.geoplugin_longitude],
    zoom: 8,
    zoomControl: false,
    doubleClickZoom: false
  })
  L.tileLayer(
    'http://rt0.map.gtimg.com/realtimerender?z={z}&x={x}&y={-y}&type=vector&style=0'
  ).addTo(map.value)
}

const option = ref({
  title: {
    text: 'Site Data',
    left: 'center'
  },
  tooltip: {
    trigger: 'item',
    formatter: '{b}: {c}'
  },
  xAxis: {
    data: ['Article count', 'User count']
  },
  yAxis: {},
  series: [
    {
      type: 'bar',
      data: [0, 0]
    }
  ]
})
</script>

<style scoped>
span {
  font-weight: bold;
}
.el-card {
  margin-top: 0px;
  margin-bottom: 10px;
}
.leaflet-container {
  height: 200px;
}
#ip {
  position: absolute;
  top: 0px;
  right: 0px;
  padding: 5px;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 0px 0px 0px 8px;
  z-index: 401;
}
.chart {
  padding-top: 10px;
  height: 230px;
  background-color: #fff;
}
.chart-container {
  height: 200px;
}
</style>
