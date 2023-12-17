<template>
  <div>
    <div class="d-flex align-items-center">
      <h5>Достижения по критериям MYP</h5>
      <simple-dropdown class="ms-auto" v-model="currentLevel" :propItems="YEAR_LEVELS" showName="name"
        :disabled="isYearDisable" />
    </div>
    <small>Экспериментальная функция</small>
    <div class="mb-2">
      <div class="accordion" :id="`accordionStrand${report.id}`">
        <div class="accordion-item" v-for="objectives, key in strandsByObjective" :key="key">
          <h2 class="accordion-header" :id="`heading${report.id}-${key}`">
            <button class="accordion-button collapsed py-1 px-2" type="button" data-bs-toggle="collapse"
              :data-bs-target="`#collapse${report.id}-${key}`" aria-expanded="true" aria-controls="collapseOne">
              <div class="my-2">{{ unitMypStore.objectives.find(i => i.id == key).full_name }} - <b
                  v-if="calculatedObjectives[key]">
                  {{ calculatedObjectives[key][0].avg_point || 'Не оценивается' }}</b></div>
            </button>
          </h2>
          <div :id="`collapse${report.id}-${key}`" class="accordion-collapse collapse"
            :aria-labelledby="`heading${report.id}-${key}`" :data-bs-parent="`#accordionStrand${report.id}`">
            <div class="accordion-body">
              <div v-for="strand in objectives" :key="strand.id">
                <div v-if="strand.level_strand">
                  <div class="d-flex align-items-center mb-2">
                    <div v-if="allowedMode">
                      <i class="bi bi-dash-square dot-menu me-2" v-if="strand.level_strand.report"
                        @click="removeReportSecondaryLevel(strand.level_strand.report.id)"></i>
                      <i class="bi bi-plus-square dot-menu me-2" v-else
                        @click="createReportSecondaryLevel(strand.level_strand.id)"></i>
                    </div>
                    <span :class="{ 'select': strand.level_strand.report }">{{ strand.letter_name }}. Students should be
                      able to
                      {{ strand.level_strand.name }}
                      <b v-if="strand.level_strand.report && strand.level_strand.report.level"> - {{
                        strand.level_strand.report.level.point }}</b>
                      <b v-if="strand.level_strand.report && !strand.level_strand.report.level"> - 0</b>
                    </span>
                  </div>
                  <div v-if="strand.level_strand.report">
                    <ul v-if="allowedMode">
                      <li>
                        <div class="pointer" :class="{ 'select': !strand.level_strand.report.level }"
                          @click="updateReportSecondaryLevel(null, strand.level_strand.report.id)">
                          The student does not reach a standard described by any of the descriptors below
                        </div>
                      </li>
                      <li v-for="achieve in strand.level_strand.report.strand.achieve_levels" :key="achieve.id"
                        @click="updateReportSecondaryLevel(achieve.id, strand.level_strand.report.id)">
                        <div class="pointer"
                          :class="{ 'select': strand.level_strand.report.level && achieve.id == strand.level_strand.report.level.id }">
                          The student {{ achieve.name }} ({{ achieve.point - 1 }}-{{ achieve.point }})
                        </div>
                      </li>
                    </ul>
                    <ul v-else>
                      <li>
                        <div :class="{ 'select': !strand.level_strand.report.level }">
                          The student does not reach a standard described by any of the descriptors below
                        </div>
                      </li>
                      <li v-for="achieve in strand.level_strand.report.strand.achieve_levels" :key="achieve.id">
                        <div
                          :class="{ 'select': strand.level_strand.report.level && achieve.id == strand.level_strand.report.level.id }">
                          The student {{ achieve.name }} ({{ achieve.point - 1 }}-{{ achieve.point }})
                        </div>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useUnitMypStore } from "@/stores/unitMyp";
import { useReportStore } from "@/stores/report";
import { YEAR_LEVELS } from "@/common/constants";
import SimpleDropdown from "@/common/components/SimpleDropdown.vue";

const props = defineProps({
  report: {
    type: Object,
    default: {},
  },
  allowedMode: {
    type: Boolean,
    default: true,
  }
});

const unitMypStore = useUnitMypStore();
const reportStore = useReportStore();

// Вспомогательная функция для проверки объекта на пустое содержимое
const isEmpty = (obj) => {
  return Object.keys(obj).length === 0;
};

const isYearDisable = computed(() => {
  return reportYear.value ? !isEmpty(reportYear.value) : false
})

const reportYear = computed(() => {
  return YEAR_LEVELS.find(i => props.report.objective_levels.length && (i.value == props.report.objective_levels[0].strand.level))
})

const currentLevel = computed(() => {
    if (reportYear.value) {
      return reportYear.value
    } else {
      if ([5, 6].includes(props.report.group.year_study.number)) {
        return YEAR_LEVELS.find(i => i.value == 1)
      } else if ([7, 8].includes(props.report.group.year_study.number)) {
        return YEAR_LEVELS.find(i => i.value == 3)
      } else if ([9].includes(props.report.group.year_study.number)) {
        return YEAR_LEVELS.find(i => i.value == 5)
      } else {
        return YEAR_LEVELS.find(i => i.value == 0)
      }
    }
  }
)

const calculatedObjectives = computed(() => {
  return groupedByCategory(unitMypStore.objectives.filter(i => i.group.id == props.report.subject.group_ib).map((item) => {
    const levels = props.report.objective_levels.filter(i => i.strand.objective == item.id).length;
    const points = props.report.objective_levels.filter(i => i.strand.objective == item.id).reduce((accumulator, item) => {
      if (item.level && item.level.point != null) {
        return accumulator + item.level.point;
      } else {
        return accumulator;
      }
    }, 0)
    return {
      ...item,
      count_level: levels,
      count_point: points,
      avg_point: points / levels,
    }
  }), 'id')
})

function groupByNestedProperty(items, key, subKey) {
  return items.reduce((accumulator, item) => {
    // Получаем ключ для группировки из вложенного свойства текущего элемента
    const groupKey = item[key][subKey];

    // Если в аккумуляторе еще нет этой группы, создаем ее
    if (!accumulator[groupKey]) {
      accumulator[groupKey] = [];
    }

    // Добавляем текущий элемент в соответствующую группу
    accumulator[groupKey].push(item);

    return accumulator;
  }, {}); // Начальное значение аккумулятора - пустой объект
}

function groupedByCategory(items, key) {
  return items.reduce((accumulator, currentItem) => {
    // Получаем ключ группировки из текущего элемента
    const groupKey = currentItem[key];

    // Если такой ключ еще не существует в аккумуляторе, создаем его
    if (!accumulator[groupKey]) {
      accumulator[groupKey] = [];
    }

    // Добавляем текущий элемент в соответствующую группу
    accumulator[groupKey].push(currentItem);

    return accumulator;
  }, {}); // Начальное значение аккумулятора - пустой объект
}

const strandsByObjective = computed(() => {
  return groupByNestedProperty(unitMypStore.strands.map(strand => {
    return {
      ...strand,
      level_strand: strand.strand_levels.map((item) => {
        return {
          ...item,
          report: props.report.objective_levels.find(
            (i) => i.strand.id == item.id
          ),
        };
      }).find(i => i.level == currentLevel.value.value)
    }
  }), 'objective', 'id')
});

// Функция редактирования конкретного поля и обновление данных из результата
const updateReportSecondaryLevel = async (value, id) => {
  console.log(
    `Сохраняемое значение для level: ${value} для записи с ID: ${id}`
  );
  const updatingData = {
    id: id,
    level: value,
  }
  reportStore.updateReportSecondaryLevel(updatingData).then((result) => {
    const index = reportStore.reportTeachers.findIndex(item => item.id === props.report.id);
    if (index != -1) {
      reportStore.reportTeachers[index].objective_levels = reportStore.reportTeachers[index].objective_levels.map(item => item.id === result.data.id ? { ...result.data } : item);
    }
  });
};

const createReportSecondaryLevel = (id) => {
  const data = {
    report: props.report.id,
    strand: id,
  };
  reportStore.createReportSecondaryLevel(data).then((result) => {
    getReportSecondaryLevels();
  });
};

// Функция запроса на удаление выбранного критерия из оценки репорта
const removeReportSecondaryLevel = (id) => {
  reportStore.removeReportSecondaryLevel(id).then(() => {
    getReportSecondaryLevels();
  });
};

// Функция запроса оценок по критериям конкретного репорта и замена этого блока в переменной reportStore
// Выполняется после добавления или удаления критерия из репорта
const getReportSecondaryLevels = () => {
  const config = {
    params: {
      report: props.report.id,
    },
  };
  reportStore.loadReportSecondaryLevels(config).then((result) => {
    const index = reportStore.reportTeachers.findIndex(
      (item) => item.id === props.report.id
    );
    reportStore.reportTeachers[index].objective_levels = [...result.data];
  });
};

</script>

<style scoped>
.select {
  font-weight: bold;
}

.pointer {
  cursor: pointer;
}

.pointer:hover {
  text-decoration: underline;
}
</style>