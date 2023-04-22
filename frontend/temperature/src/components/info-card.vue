<template>
  <div
    class="relative flex flex-col bg-clip-border rounded-xl bg-white text-gray-700 shadow-md"
  >
    <div
      class="bg-clip-border mx-4 rounded-xl overflow-hidden bg-gradient-to-tr from-blue-600 to-blue-400 text-white shadow-blue-500/40 shadow-lg absolute -mt-4 grid h-16 w-16 place-items-center"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 32 35"
        fill="currentColor"
        aria-hidden="true"
        class="w-10 h-10 text-white"
      >
        <title>temperature-high</title>
        <path
          d="M20.75 6.008c0-6.246-9.501-6.248-9.5 0v13.238c-1.235 1.224-2 2.921-2 4.796 0 3.728 3.022 6.75 6.75 6.75s6.75-3.022 6.75-6.75c0-1.875-0.765-3.572-2-4.796l-0.001-0zM16 29.25c-2.9-0-5.25-2.351-5.25-5.251 0-1.553 0.674-2.948 1.745-3.909l0.005-0.004 0.006-0.012c0.13-0.122 0.215-0.29 0.231-0.477l0-0.003c0.001-0.014 0.007-0.024 0.008-0.038l0.006-0.029v-13.52c-0.003-0.053-0.005-0.115-0.005-0.178 0-1.704 1.381-3.085 3.085-3.085 0.060 0 0.12 0.002 0.179 0.005l-0.008-0c0.051-0.003 0.11-0.005 0.17-0.005 1.704 0 3.085 1.381 3.085 3.085 0 0.063-0.002 0.125-0.006 0.186l0-0.008v13.52l0.006 0.029 0.007 0.036c0.015 0.191 0.101 0.36 0.231 0.482l0 0 0.006 0.012c1.076 0.966 1.75 2.361 1.75 3.913 0 2.9-2.35 5.25-5.25 5.251h-0zM16.75 21.367v-15.367c0-0.414-0.336-0.75-0.75-0.75s-0.75 0.336-0.75 0.75v0 15.367c-1.164 0.338-2 1.394-2 2.646 0 1.519 1.231 2.75 2.75 2.75s2.75-1.231 2.75-2.75c0-1.252-0.836-2.308-1.981-2.641l-0.019-0.005zM26.5 2.25c-1.795 0-3.25 1.455-3.25 3.25s1.455 3.25 3.25 3.25c1.795 0 3.25-1.455 3.25-3.25v0c-0.002-1.794-1.456-3.248-3.25-3.25h-0zM26.5 7.25c-0.966 0-1.75-0.784-1.75-1.75s0.784-1.75 1.75-1.75c0.966 0 1.75 0.784 1.75 1.75v0c-0.001 0.966-0.784 1.749-1.75 1.75h-0z"
        ></path>
      </svg>

      <!-- <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="currentColor"
        aria-hidden="true"
        class="w-6 h-6 text-white"
      >
        <path d="M12 7.5a2.25 2.25 0 100 4.5 2.25 2.25 0 000-4.5z"></path>
        <path
          fill-rule="evenodd"
          d="M1.5 4.875C1.5 3.839 2.34 3 3.375 3h17.25c1.035 0 1.875.84 1.875 1.875v9.75c0 1.036-.84 1.875-1.875 1.875H3.375A1.875 1.875 0 011.5 14.625v-9.75zM8.25 9.75a3.75 3.75 0 117.5 0 3.75 3.75 0 01-7.5 0zM18.75 9a.75.75 0 00-.75.75v.008c0 .414.336.75.75.75h.008a.75.75 0 00.75-.75V9.75a.75.75 0 00-.75-.75h-.008zM4.5 9.75A.75.75 0 015.25 9h.008a.75.75 0 01.75.75v.008a.75.75 0 01-.75.75H5.25a.75.75 0 01-.75-.75V9.75z"
          clip-rule="evenodd"
        ></path>
        <path
          d="M2.25 18a.75.75 0 000 1.5c5.4 0 10.63.722 15.6 2.075 1.19.324 2.4-.558 2.4-1.82V18.75a.75.75 0 00-.75-.75H2.25z"
        ></path>
      </svg> -->
    </div>
    <div class="p-4 text-right">
      <p
        class="block antialiased font-sans text-sm leading-normal font-normal text-blue-gray-600"
      >
        {{ title }}
      </p>
      <p
        class="block antialiased tracking-normal font-sans text-2xl font-semibold leading-snug text-black"
      >
        {{ temperature }} °C
      </p>
      <div class="border-t border-blue p4">
        <p
          class="block antialiased font-sans text-base leading-relaxed font-normal text-blue-gray-600"
        >
          <strong class="text-green-500">{{ sign }}{{ difference }} °C </strong>
          <span class="text-gray-400"> {{ description }}</span>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "InfoCard",

  components: {},

  props: {
    temperature: {
      type: Number,
      default: 0,
    },
    title: {
      type: String,
      default: "",
    },
    description: {
      type: String,
      default: "",
    },
    difference: {
      type: String,
      default: "",
    },
    sign: {
      type: String,
      default: "",
    },
  },

  data: function () {
    return {};
  },

  methods: {},
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
 