from playwright.sync_api import sync_playwright
import time

url = 'file:///Users/hailingdediannao/CodeBuddy/20260924015331/prototype/activity-all.html'


def snapshot(page):
    return page.evaluate('''() => {
      const activePage = document.querySelector('.page:not(.hidden)');
      const firstMenuGroup = document.querySelector('.menu-group');
      return {
        activePageId: activePage ? activePage.id : null,
        toastDisplay: document.getElementById('toast').style.display,
        toastText: document.getElementById('toast').textContent,
        modalCount: document.querySelectorAll('.modal-mask.show').length,
        firstMenuOpen: firstMenuGroup ? firstMenuGroup.classList.contains('open') : null,
        basicCollapsed: document.getElementById('basicHeader')?.classList.contains('collapsed'),
        basicBodyDisplay: document.getElementById('basicBody')?.style.display,
        ruleSetCollapsed: document.getElementById('ruleSet1')?.classList.contains('collapsed'),
        ruleSetBodyDisplay: document.getElementById('ruleSet1Body')?.style.display,
        libSearchCollapsed: document.getElementById('lib-searchHeader')?.classList.contains('collapsed'),
        libSearchBodyDisplay: document.getElementById('lib-searchBody')?.style.display,
        libResultCollapsed: document.getElementById('lib-resultHeader')?.classList.contains('collapsed'),
        dataSearchCollapsed: document.getElementById('data-searchHeader')?.classList.contains('collapsed'),
        dataResultCollapsed: document.getElementById('data-resultHeader')?.classList.contains('collapsed'),
        switchLabel: document.getElementById('switchLabel')?.textContent,
        ruleSetExists: !!document.getElementById('ruleSet1'),
      };
    }''')


def click_test(page, name, selector, need_visible=False):
    before = snapshot(page)
    result = page.evaluate('''(args) => {
      const [sel, needVisible] = args;
      const el = document.querySelector(sel);
      if (!el) return '元素不存在';
      if (needVisible) {
        const rect = el.getBoundingClientRect();
        if (rect.width === 0 || rect.height === 0) return '元素无尺寸';
      }
      try { el.click(); } catch (e) { return '点击异常 ' + e.message; }
      return 'OK';
    }''', [selector, need_visible])
    if result != 'OK':
        return f'{name}: {result}'
    time.sleep(0.25)
    after = snapshot(page)
    changed = any(after[k] != before[k] for k in before)
    return f'{name}: {"有响应" if changed else "无响应"}'


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        logs = []
        page.on('console', lambda msg: logs.append(f'[{msg.type}] {msg.text}'))
        page.on('pageerror', lambda err: logs.append(f'[pageerror] {err}'))
        page.on('dialog', lambda dialog: dialog.accept())
        page.goto(url)
        page.wait_for_load_state('networkidle')
        time.sleep(0.5)

        results = []

        results.append('=== 全局导航 ===')
        results.append(click_test(page, '菜单-活动分润规则管理', '.sub-menu a[data-page="page-rule"]'))
        results.append(click_test(page, '菜单-配置规则条件库', '.sub-menu a[data-page="page-lib"]'))
        results.append(click_test(page, '菜单-活动分润数据管理', '.sub-menu a[data-page="page-data"]'))
        results.append(click_test(page, 'Tab-活动分润规则管理', '.tabs-bar .tab-item[data-page="page-rule"]'))
        results.append(click_test(page, 'Tab-配置规则条件库', '.tabs-bar .tab-item[data-page="page-lib"]'))
        results.append(click_test(page, 'Tab-活动分润数据管理', '.tabs-bar .tab-item[data-page="page-data"]'))
        results.append(click_test(page, '左侧菜单折叠', '.menu-title'))

        results.append('\n=== 活动分润规则管理列表 ===')
        results.append(click_test(page, '创建活动分润规则', '#btnCreateRule'))
        results.append(click_test(page, '列表-重置', '#page-rule-list .search-card .btn'))
        results.append(click_test(page, '列表-查询', '#page-rule-list .search-card .btn-primary'))
        results.append(click_test(page, '列表-查看详情', '#page-rule-list .data-table .ops a:nth-child(1)'))
        results.append(click_test(page, '列表-停用', '#page-rule-list .data-table .ops a:nth-child(2)'))
        results.append(click_test(page, '列表-删除', '#page-rule-list .data-table .ops a:nth-child(3)'))
        results.append(click_test(page, '分页-1', '#page-rule-list .page-btn.active'))

        results.append('\n=== 创建活动分润规则 ===')
        page.evaluate('() => document.getElementById("btnCreateRule").click()')
        time.sleep(0.3)
        results.append(click_test(page, '创建页-基本信息折叠', '#basicHeader'))
        results.append(click_test(page, '创建页-规则集折叠', '#ruleSet1 .rule-block-header'))
        results.append(click_test(page, '创建页-活动开关', '#activitySwitch'))
        results.append(click_test(page, '创建页-重命名', '#btnRename'))
        results.append(click_test(page, '创建页-导入机构', '#btnImportOrg'))
        results.append(click_test(page, '创建页-下载模板', '#page-create a.link'))
        # select 需要真实选择才能触发 change，click 本身不会展开并选择
        results.append(click_test(page, '创建页-规则类型下拉', '#ruleTypeSelect'))
        results.append(click_test(page, '创建页-新增规则集', '#addRuleSet'))
        results.append(click_test(page, '创建页-导入设备SN', '#btnImportSn'))
        results.append(click_test(page, '创建页-删除规则集', '#btnDelete'))
        results.append(click_test(page, '创建页-取消', '#btnCancel'))
        page.evaluate('() => document.getElementById("btnCreateRule").click()')
        time.sleep(0.3)
        results.append(click_test(page, '创建页-保存', '#btnSave'))

        results.append('\n=== 配置规则条件库 ===')
        page.evaluate('() => document.querySelector(".sub-menu a[data-page=page-lib]").click()')
        time.sleep(0.3)
        results.append(click_test(page, '规则库-查询区折叠', '#lib-searchHeader'))
        results.append(click_test(page, '规则库-结果区折叠', '#lib-resultHeader'))
        results.append(click_test(page, '规则库-查询', '#lib-btnSearch'))
        results.append(click_test(page, '规则库-重置', '#lib-btnReset'))
        results.append(click_test(page, '规则库-导出', '#lib-btnExport'))
        results.append(click_test(page, '规则库-下载模板', '#lib-btnDownloadTemplate'))
        results.append(click_test(page, '规则库-创建', '#lib-btnCreate'))
        results.append(click_test(page, '规则库-弹窗关闭', '#lib-btnCloseModal', need_visible=True))
        # 重新打开弹窗再测取消/确认
        page.evaluate('() => document.getElementById("lib-btnCreate").click()')
        time.sleep(0.2)
        results.append(click_test(page, '规则库-弹窗取消', '#lib-btnCancelModal', need_visible=True))
        page.evaluate('() => document.getElementById("lib-btnCreate").click()')
        time.sleep(0.2)
        results.append(click_test(page, '规则库-弹窗确认', '#lib-btnConfirm', need_visible=True))
        results.append(click_test(page, '规则库-表格查看详情', '#lib-ruleTableBody .action-detail'))
        results.append(click_test(page, '规则库-表格历史记录', '#lib-ruleTableBody .action-history'))
        results.append(click_test(page, '规则库-表格删除', '#lib-ruleTableBody .action-delete'))

        results.append('\n=== 活动分润数据管理 ===')
        page.evaluate('() => document.querySelector(".sub-menu a[data-page=page-data]").click()')
        time.sleep(0.3)
        results.append(click_test(page, '数据-查询区折叠', '#data-searchHeader'))
        results.append(click_test(page, '数据-结果区折叠', '#data-resultHeader'))
        results.append(click_test(page, '数据-查询', '#data-btnSearch'))
        results.append(click_test(page, '数据-重置', '#data-btnReset'))
        results.append(click_test(page, '数据-明细导出', '#data-btnDetailExport'))
        results.append(click_test(page, '数据-导出', '#data-btnExport'))
        results.append(click_test(page, '数据-新建跑批', '#data-btnNewBatch'))
        results.append(click_test(page, '数据-跑批记录', '#data-btnBatchRecord'))

        if logs:
            results.append('\n=== 控制台日志 ===')
            results.extend(logs)

        browser.close()

        for r in results:
            print(r)


if __name__ == '__main__':
    main()
