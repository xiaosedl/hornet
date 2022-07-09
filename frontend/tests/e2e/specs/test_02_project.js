// https://docs.cypress.io/api/introduction/api.html

describe("Test project", () => {
  it("create", () => {
    let timestamp = Date.parse(new Date());
    cy.visit("/main/project");
    cy.get("[cy-data=ProjectCreate]", { timeout: 3000 }).click();
    cy.get("[cy-data=ProjectName]", { timeout: 3000 }).type(
      "项目名称 " + timestamp
    );
    cy.get("[cy-data=ProjectDescribe]", { timeout: 3000 }).type("项目描述");
    cy.get("[cy-data=ProjectSubmit]").click();
  });
  it("edit", () => {
    let timestamp = Date.parse(new Date());
    cy.visit("/main/project");
    cy.get("[cy-data=ProjectSetting]", { timeout: 3000 })
      .eq(1)
      .click({ force: true });
    cy.get("[cy-data=ProjectEdit]", { timeout: 3000 })
      .eq(1)
      .click({ force: true });
    cy.get("[cy-data=ProjectName]", { timeout: 3000 })
      .clear()
      .type("项目名称 " + timestamp);
    cy.get("[cy-data=ProjectDescribe]", { timeout: 3000 })
      .clear()
      .type("项目描述");
    cy.get("[cy-data=ProjectSubmit]").click();
  });
  it("delete", function () {
    cy.visit("/main/project");
    cy.get("[cy-data=ProjectSetting]", { timeout: 3000 })
      .eq(-1)
      .click({ force: true });
    cy.get("[cy-data=ProjectDelete]", { timeout: 3000 })
      .eq(1)
      .click({ force: true });
    cy.contains("p", "删除成功");
  });
  it("page", function () {
    cy.visit("/main/project");
    cy.get("[cy-data=ProjectPage] > ul.el-pager > li.number", { timeout: 3000 })
      .eq(1)
      .click();
    cy.get("[cy-data=ProjectPage] > button.btn-next", {
      timeout: 3000,
    }).click();
  });
});
