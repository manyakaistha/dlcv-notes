(function () {
  'use strict';

  var PARAM_TOPIC = 'topic';
  var PARAM_YEAR = 'year';
  var PARAM_DEDUP = 'dedup';

  var bar = document.querySelector('.qfilter');
  if (!bar) return;

  var topicSel = document.getElementById('qf-topic');
  var yearSel = document.getElementById('qf-year');
  var dedupBox = document.getElementById('qf-dedup');
  var resetBtn = document.getElementById('qf-reset');
  var countEl = document.getElementById('qf-count');

  // Static inventory, computed once in document order.
  var allItems = Array.prototype.slice.call(document.querySelectorAll('.qitem'));
  var nodes = Array.prototype.slice.call(document.querySelectorAll('h2, .qitem'));

  var groupSize = {};
  allItems.forEach(function (item) {
    var g = groupKey(item);
    if (g !== null) groupSize[g] = (groupSize[g] || 0) + 1;
  });

  function groupKey(item) {
    var g = item.getAttribute('data-group');
    return g === null || g === '' ? null : g;
  }

  function topicsOf(item) {
    var raw = item.getAttribute('data-topics') || '';
    return raw.split('|').map(function (s) { return s.trim(); });
  }

  function passes(item, topic, year) {
    if (topic && topicsOf(item).indexOf(topic) === -1) return false;
    if (year && item.getAttribute('data-year') !== year) return false;
    return true;
  }

  function clearBadges() {
    var old = document.querySelectorAll('.qdup-badge');
    for (var i = 0; i < old.length; i++) old[i].parentNode.removeChild(old[i]);
  }

  function makeBadge(item) {
    var g = groupKey(item);
    if (g === null || groupSize[g] < 2) return null;
    var labels = allItems
      .filter(function (other) { return groupKey(other) === g; })
      .map(function (other) { return other.getAttribute('data-label') || other.getAttribute('data-qid') || ''; });
    var p = document.createElement('p');
    p.className = 'qdup-badge';
    p.textContent = 'Asked ' + labels.length + ' times: ' + labels.join(' · ');
    return p;
  }

  function applyHeadings() {
    var current = null;
    var hasItems = false;
    var anyVisible = false;
    function flush() {
      if (!current) return;
      current.hidden = hasItems ? !anyVisible : false;
    }
    nodes.forEach(function (node) {
      if (node.tagName === 'H2') {
        flush();
        current = node;
        hasItems = false;
        anyVisible = false;
      } else {
        hasItems = true;
        if (!node.hidden) anyVisible = true;
      }
    });
    flush();
  }

  function readControls() {
    return {
      topic: topicSel ? topicSel.value : '',
      year: yearSel ? yearSel.value : '',
      dedup: !!(dedupBox && dedupBox.checked)
    };
  }

  function writeState(state) {
    try {
      var params = new URLSearchParams();
      if (state.topic) params.set(PARAM_TOPIC, state.topic);
      if (state.year) params.set(PARAM_YEAR, state.year);
      if (state.dedup) params.set(PARAM_DEDUP, '1');
      var qs = params.toString();
      var url = location.pathname + (qs ? '?' + qs : '') + location.hash;
      history.replaceState(history.state, '', url);
    } catch (e) {
      // URL state is optional; ignore environments that forbid replaceState.
    }
  }

  function readState() {
    try {
      var params = new URLSearchParams(location.search);
      var topic = params.get(PARAM_TOPIC) || '';
      var year = params.get(PARAM_YEAR) || '';
      if (topicSel) {
        topicSel.value = topic;
        if (topicSel.value !== topic) topicSel.value = '';
      }
      if (yearSel) {
        yearSel.value = year;
        if (yearSel.value !== year) yearSel.value = '';
      }
      if (dedupBox) dedupBox.checked = params.get(PARAM_DEDUP) === '1';
    } catch (e) {
      // Malformed or unavailable query string: fall back to defaults.
    }
  }

  function render() {
    var state = readControls();

    // Pass 1: filter by topic and year.
    var passing = allItems.filter(function (item) {
      return passes(item, state.topic, state.year);
    });

    // Pass 2: keep the last passing item per duplicate group.
    var lastByGroup = {};
    passing.forEach(function (item) {
      var g = groupKey(item);
      if (g !== null) lastByGroup[g] = item;
    });

    var shown = 0;
    allItems.forEach(function (item) {
      var isPassing = passing.indexOf(item) !== -1;
      var g = groupKey(item);
      var visible = isPassing &&
        (!state.dedup || g === null || lastByGroup[g] === item);
      item.hidden = !visible;
      if (visible) shown += 1;
    });

    // Badges: only on visible items, only when deduplicating.
    clearBadges();
    if (state.dedup) {
      allItems.forEach(function (item) {
        if (item.hidden) return;
        var badge = makeBadge(item);
        if (!badge) return;
        var h3 = item.querySelector('h3');
        if (h3) {
          h3.parentNode.insertBefore(badge, h3.nextSibling);
        } else {
          item.insertBefore(badge, item.firstChild);
        }
      });
    }

    applyHeadings();

    if (countEl) {
      if (shown === 0) {
        countEl.textContent = 'No questions match these filters.';
      } else {
        countEl.textContent = 'Showing ' + shown + ' of ' + allItems.length + ' questions' +
          (state.dedup ? ' (duplicates merged)' : '');
      }
    }

    writeState(state);
  }

  function clearAll() {
    if (topicSel) topicSel.value = '';
    if (yearSel) yearSel.value = '';
    if (dedupBox) dedupBox.checked = false;
    render();
  }

  function handleHash() {
    var id;
    try {
      id = decodeURIComponent(location.hash.slice(1));
    } catch (e) {
      return;
    }
    if (!id) return;
    var el = document.getElementById(id);
    if (!el) return;
    var item = el.closest('.qitem');
    if (!item || !item.hidden) return;
    clearAll();
    el.scrollIntoView({ block: 'center' });
  }

  function init() {
    readState();
    render();
    handleHash();

    if (topicSel) topicSel.addEventListener('change', render);
    if (yearSel) yearSel.addEventListener('change', render);
    if (dedupBox) dedupBox.addEventListener('change', render);
    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        clearAll();
      });
    }
    window.addEventListener('hashchange', handleHash);
  }

  if (document.readyState !== 'loading') {
    init();
  } else {
    document.addEventListener('DOMContentLoaded', init);
  }
})();
