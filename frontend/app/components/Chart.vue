<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  BarController,
  LineElement,
  LineController,
  PointElement,
  ArcElement,
  DoughnutController,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'
import type { ChartConfiguration } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, BarController, LineElement, LineController, PointElement, ArcElement, DoughnutController, Title, Tooltip, Legend, Filler)

const props = withDefaults(
  defineProps<{
    type: 'bar' | 'line' | 'doughnut' | 'pie'
    data: Record<string, unknown>
    options?: Record<string, unknown>
    height?: number
  }>(),
  { type: 'bar', height: 240 },
)

const canvasRef = ref<HTMLCanvasElement | null>(null)
let chart: ChartJS | null = null

const initChart = () => {
  if (!canvasRef.value) return
  const ctx = canvasRef.value.getContext('2d')
  if (!ctx) return

  const config: ChartConfiguration = {
    type: props.type as ChartConfiguration['type'],
    data: props.data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: props.type === 'doughnut' || props.type === 'pie' },
        tooltip: {
          callbacks: {
            label: (ctx: any) => {
              return `${ctx.dataset.label || ''}: $${ctx.parsed.y?.toFixed(2) || ctx.formattedValue}`
            },
          },
        },
      },
      scales: props.type === 'bar' || props.type === 'line'
        ? {
            x: { grid: { display: false } },
            y: { grid: { color: 'rgb(226 232 240 / 0.5)' }, ticks: { color: '#94a3a4', font: { size: 11 } } },
          }
        : undefined,
      ...props.options,
    },
  }

  chart = new ChartJS(ctx, config)
}

const updateChart = () => {
  if (!chart) return
  chart.data = props.data
  if (props.options) chart.options = { ...chart.options, ...props.options }
  chart.update()
}

onMounted(initChart)
onBeforeUnmount(() => chart?.destroy())

watch(() => props.data, updateChart, { deep: true })
watch(() => props.options, updateChart, { deep: true })
</script>

<template>
  <div :style="{ height: `${height}px` }">
    <canvas ref="canvasRef" />
  </div>
</template>

<style scoped>
canvas {
  display: block;
}
</style>
