package {{config.core_base_package}}.test.service.{{config.package_sysname}}.{{module.moduleName}};

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Assert;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.springframework.beans.factory.annotation.Autowired;

import {{config.core_base_package}}.test.base.AbstractServiceTest;
import {{config.core_base_package}}.facade.bean.dubbo.{{config.package_sysname}}.{{module.moduleName}}.{{service.className}}Req;
import {{config.core_base_package}}.facade.bean.dubbo.{{config.package_sysname}}.{{module.moduleName}}.{{service.className}}Resp;
import {{config.core_base_package}}.service.crm.impl.{{config.package_sysname}}.{{module.moduleName}}.{{config.core_base_service_prefix}}{{service.className}}Service;
import {{config.core_base_package}}.service.crm.impl.lcsapp.login.LcsAppCrmLoginService;
import {{config.core_base_package}}.service.crm.impl.lcsapp.login.LcsAppCrmLogoutService;
import {{config.core_base_package}}.test.base.JSONFormatUtil;
import {{config.core_base_package}}.test.base.ServiceTestUtil;

/**
* ClassName: {{config.core_base_service_prefix}}{{service.className}}ServiceTest <br/>
* Function: {{service.desc}}单体测试类. <br/>
* Reason: TODO ADD REASON. <br/>
* Date: {{module.codeCreateTime}} <br/>
*
* @author {{config.author}}
* @version
* @since JDK 1.7
* Copyright (c) 2017, www.leadfund.com.cn All Rights Reserved.
* 上海利得金融科技集团版权所有.
*/
public class {{config.core_base_service_prefix}}{{service.className}}ServiceTest extends AbstractServiceTest {

@Autowired
private {{config.core_base_service_prefix}}{{service.className}}Service m{{service.className}}Service;

@Autowired
private LcsAppCrmLoginService mLoginService;

@Autowired
private LcsAppCrmLogoutService mLogoutService;

/**
* mPropList: 用于插入或更新的属性一览.
* @since JDK 1.7
*/
{{service.className}}Req mReq = null;

@BeforeClass
public static void setUpBeforeClass() throws Exception {}

@AfterClass
public static void tearDownAfterClass() throws Exception {}

/**
* setUp: 测试数据对象初始化.
*
* @author {{config.author}}
* @throws Exception
* @since JDK 1.7
*/
@Before
public void setUp() throws Exception {
// 生成需要插入更新的属性
mReq = new {{service.className}}Req();
ServiceTestUtil.setLcsAppCommonRequest(mReq);
}

@After
public void tearDown() throws Exception {}

@Test
public void test() {
// 用户登录
String lToken = ServiceTestUtil.defaultLogin(mLoginService);;
mReq.setToken(lToken);

System.out.println(JSONFormatUtil.formatObject(mReq));
// 测试参数校验
m{{service.className}}Service.verifyParameter(mReq);

// 测试逻辑处理
{{service.className}}Resp lResp = ({{service.className}}Resp)m{{service.className}}Service.handle(mReq);
System.out.println(JSONFormatUtil.formatObject(lResp));

//junit assert
Assert.assertNotNull(lResp);

// 退出登录
ServiceTestUtil.logout(mLogoutService, lToken);
}
}