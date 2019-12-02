Vue.component('tag-commits', {
  props: {
    'commits': {
      required: true
    }
  },
  template: `
  <tr>
    <td></td> <!-- intentionally left blank -->
    <td colspan=8>
      <ul class="commit-data">
        <li v-for="commit in commits" :key="commit.git_hash" class="commit-subject">
          {{ commit.subject }} <span class="author-data">- {{ commit.author_name }}</span>
          <ul>
            <li v-for="rnd in commit.rn_data" class="releasenote-data">
              {{ rnd.codes }}=<span v-html="toUrl(rnd.issue_id)" /> <em><span v-html="toUrl(rnd.comment)" /></em>
            </li>
          </ul>
        </li>
      </ul>
    </td>
  </tr>
  `,
  methods: {
    toUrl: function(text) {
      let systems = {
        jira: {
          regex: /((?:GROUP|TEAM|DEPT)-[0-9]+)/,
          convert: function(id) {
            return "https://jira.company.website/browse/" + id;
          }
        },
        internal-tool: {
          regex: /(ISS[0-9]+|XX[0-9]+|BAD-[0-9]+-[A-Z0-9]{4})/,
          convert: function(id) {
            return "https://tickets.company.website/tickets/issueReport.html?id=" + id;
          }
        }
      }
      // TODO: accomodate several links
      for (let name in systems) {
        if (systems[name].regex.test(text)) {
          let id = systems[name].regex.exec(text)[0];
          let url = systems[name].convert(id);
          let link = '<a href="' + url + '" target="_blank">' + id + '</a>';
          return text.replace(id, link)
        }
      }
      return text
    }
  }
})

Vue.component('tag-detail', {
  template: `
    <tr class="commit-row">
      <td><button @click="toggleCommits">+</button></td>
      <td>{{ tag.branch.name }}</td>
      <td><a :href="downloadHref">{{ tag.name }}</a></td>
      <td>{{ lastAuthor }}</td>
      <td :class="{ highlight: updated.dependency1_version }">{{ tag.dependency1_version }}</td>
      <td :class="{ highlight: updated.dependency2_version }">{{ tag.dependency2_version }}</td>
      <td :class="{ highlight: updated.dependency3_version }">{{ tag.dependency3_version }}</td>
      <td>{{ tag.release_time }}</td>
      <td><a :href="releaseNoteXml">Release note</a> /
          <a :href="rnLink" target="_blank">RNT</a></td>
    </tr>
  `,
  props: {
    tag: {
      required: true
    }
  },
  methods: {
    toggleCommits() {
      this.$emit("toggle-commits", this.hash);
    }
  },
  computed: {
    downloadHref: function () {
      return "https://gerrit.company.website/gerrit/gitweb?p=DIV/DEPT/TEAM/repo.git;a=log;h=refs/tags/" + this.tag.name
    },
    releaseNoteXml: function () {
      return "https://rnt.company.website/download/releasenote/" + this.tag.name + ".xml"
    },
    rntLink: function () {
      return "https://rnt.company.website/dept/team/releases/" + this.tag.name
    },
    lastAuthor: function () {
      return this.tag.commits[0].author_name;
    },
    hash: function () {
      return this.tag.commits[0].git_hash;
    },
    updated: function() {
      return {
        dependency1_version: this.tag.dependency1_version !== this.tag.parent.dependency1_version,
        dependency2_version: this.tag.dependency2_version !== this.tag.parent.dependency2_version,
        dependency3_version: this.tag.dependency3_version !== this.tag.parent.dependency3_version,
      }
    }
  }
})

var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data() {
    return {
      info: "",
      expanded: [],
      all_toggled: false,
      reloaded: 0,
      pagination: {
        number: 1,
        size: 10,
      },
      filter: {
        issue_id: "",
        branch: "",
        name: "",
        author: "",
        dependency1_version: "",
        dependency2_version: "",
        dependency3_version: "",
        release_time: "",
        order: "",
      }
    }
  },
  methods: {
    refresh() {
      this.reloaded += 1;
      axios
        .get('/tag-table/list/',
          {params: this.query_params}
        )
        .then(response => (this.info = response))
    },
    sortField(field) {
      let reverseField = '-' + field;
      if (this.filter.order === reverseField) {
        this.filter.order = "";
      } else if (this.filter.order === field) {
        this.filter.order = reverseField
      } else {
        this.filter.order = field;
      }
      this.refresh();
    },
    toggleAll() {
      if (this.all_toggled) {
        this.expanded = [];
        this.all_toggled = false;
      } else {
        for (let tag of this.info.data.results) {
          let commit_hash = tag.commits[0].git_hash;
          if (this.expanded.indexOf(commit_hash) == -1) {
            this.expanded.push(commit_hash);
          }
          this.all_toggled = true;
        }
      }
    },
    toggleCommits(git_hash) {
      let idx = this.expanded.indexOf(git_hash);
      if (idx == -1) {
        this.expanded.push(git_hash);
      } else {
        this.expanded.splice(idx, 1);
      }
    },
    setPage(valid, page_number) {
      if (valid) {
        this.pagination.number = page_number;
        this.expanded = [];
        this.refresh();
      }
    },
    firstPage() {
      this.setPage(this.info.data.previous, 1);
    },
    previousPage() {
      this.setPage(this.info.data.previous, this.pagination.number - 1);
    },
    nextPage() {
      this.setPage(this.info.data.next, this.pagination.number + 1);
    },
    lastPage() {
      this.setPage(this.info.data.next, this.total_pages);
    },
    resetPageSize() {
      this.pagination.number = Math.min(this.pagination.number, this.total_pages);
      this.refresh();
    },
    updateFilters() {
      this.pagination.number = 1;
      this.refresh();
    }
  },
  mounted () {
    axios
      .get('/tag-table/list/')
      .then(response => (this.info = response))
  },
  computed: {
    query_params: function () {
      params = {};
      for (let field in this.filter) {
        if (this.filter[field] != "") {
          params[field] = this.filter[field];
        }
      }
      params["page"] = this.pagination.number
      params["page-size"] = this.pagination.size
      return params
    },
    total_pages: function() {
      if (this.info.data.count === null) {
        return 1;
      }
      return Math.ceil(this.info.data.count / this.pagination.size);
    }
  }
})
