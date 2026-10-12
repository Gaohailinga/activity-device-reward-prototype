function $(id) {
  return document.getElementById(id);
}

function showToast(message, duration = 2000) {
  const toast = $('toast');
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), duration);
}

function showPage(pageId) {
  let targetId = pageId;
  if (!$(targetId)) {
    targetId = 'page-' + pageId;
  }
  if (!$(targetId)) return;

  document.querySelectorAll('.page').forEach((el) => el.classList.add('hidden'));
  $(targetId).classList.remove('hidden');

  document.querySelectorAll('.tab').forEach((tab) => tab.classList.remove('active'));
  const activeTab = document.querySelector(`.tab[data-page="${pageId}"], .tab[data-page="${targetId}"]`);
  if (activeTab) activeTab.classList.add('active');

  document.querySelectorAll('.sub-menu a').forEach((a) => a.classList.remove('active'));
  const activeMenu = document.querySelector(`.sub-menu a[data-page="${pageId}"], .sub-menu a[data-page="${targetId}"]`);
  if (activeMenu) activeMenu.classList.add('active');
}

function openModal(id) {
  $(id).classList.remove('hidden');
}

function closeModal(id) {
  $(id).classList.add('hidden');
}

function bindPageSwitch() {
  document.querySelectorAll('[data-page]').forEach((el) => {
    el.addEventListener('click', (e) => {
      const pageId = el.getAttribute('data-page');
      if (pageId) {
        e.preventDefault();
        showPage(pageId);
      }
    });
  });
}

// 创建普通活动分润规则
$('btn-create-rule').addEventListener('click', () => {
  showToast('普通活动创建页暂未在本次范围');
});

// 创建设备分润规则
$('btn-create-device').addEventListener('click', () => {
  showPage('page-device-create');
});

// 创建设备分润规则：取消返回列表
$('btn-device-cancel').addEventListener('click', () => {
  showPage('page-rule-list');
});

// 创建设备分润规则：保存
$('btn-device-save').addEventListener('click', () => {
  showToast('保存成功');
  setTimeout(() => showPage('page-rule-list'), 800);
});

// 创建2026年机具奖励规则
$('btn-create-2026').addEventListener('click', () => {
  showPage('page-2026-create');
});

// 2026年规则：取消返回列表
$('btn-2026-cancel').addEventListener('click', () => {
  showPage('page-rule-list');
});

// 2026年规则：保存
$('btn-2026-save').addEventListener('click', () => {
  showToast('保存成功');
  setTimeout(() => showPage('page-rule-list'), 800);
});

// 2026年规则上传Excel模拟
if ($('btn-upload-sn-2026')) {
  $('btn-upload-sn-2026').addEventListener('click', () => {
    showToast('已导入设备序列号文件');
    $('sn-preview-2026').style.display = 'block';
  });
}

// 新建跑批弹窗
$('btn-new-batch').addEventListener('click', () => {
  openModal('modal-batch');
});

$('btn-batch-cancel').addEventListener('click', () => {
  closeModal('modal-batch');
});

$('modal-batch-close').addEventListener('click', () => {
  closeModal('modal-batch');
});

$('btn-batch-submit').addEventListener('click', () => {
  closeModal('modal-batch');
  showToast('跑批任务已提交');
});

$('modal-batch').addEventListener('click', (e) => {
  if (e.target.classList.contains('modal-mask')) {
    closeModal('modal-batch');
  }
});

// 左侧菜单折叠
function bindMenuToggle() {
  document.querySelectorAll('.menu-title').forEach((title) => {
    title.addEventListener('click', () => {
      const group = title.closest('.menu-group');
      group.classList.toggle('open');
      const icon = title.querySelector('.icon use');
      if (icon) {
        icon.setAttribute('href', group.classList.contains('open') ? '#icon-arrow-down' : '#icon-arrow-right');
      }
    });
  });
}

// 上传 Excel 模拟
$('btn-upload-sn').addEventListener('click', () => {
  showToast('已导入设备序列号文件');
  $('sn-preview').style.display = 'block';
});

// 根据 URL hash 切换页面
function switchPageByHash() {
  const hash = location.hash.replace('#', '');
  if (hash && $(hash)) {
    showPage(hash);
  }
}

window.addEventListener('hashchange', switchPageByHash);

// 初始化
bindPageSwitch();
bindMenuToggle();
switchPageByHash();
