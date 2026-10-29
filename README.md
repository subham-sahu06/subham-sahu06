subham@subham-Nitro-ANV15-41:~/checkstyle$ grep -n -i -C 3 'jacoco\|offline' pom.xml
206-    <spotbugs.plugin.version>4.10.5.0</spotbugs.plugin.version>
207-    <pmd.plugin.version>3.28.0</pmd.plugin.version>
208-    <pmd.version>7.27.0</pmd.version>
209:    <jacoco.plugin.version>0.8.15</jacoco.plugin.version>
210-    <mockito.version>5.2.0</mockito.version>
211-    <slf4j.version>2.0.20</slf4j.version>
212-    <saxon.version>13.1</saxon.version>
--
471-      <scope>runtime</scope>
472-    </dependency>
473-    <dependency>
474:      <groupId>org.jacoco</groupId>
475:      <artifactId>org.jacoco.agent</artifactId>
476:      <version>${jacoco.plugin.version}</version>
477-      <classifier>runtime</classifier>
478-      <scope>test</scope>
479-    </dependency>
--
1117-      </plugin>
1118-
1119-      <plugin>
1120:        <groupId>org.jacoco</groupId>
1121:        <artifactId>jacoco-maven-plugin</artifactId>
1122:        <version>${jacoco.plugin.version}</version>
1123-        <executions>
1124-          <execution>
1125-            <id>default-instrument</id>
--
1855-        <configuration>
1856-          <useModulePath>false</useModulePath>
1857-          <systemPropertyVariables>
1858:            <jacoco-agent.destfile>${project.build.directory}/jacoco.exec</jacoco-agent.destfile>
1859-            <!-- Virtual AWT driver for GUI unit tests -->
1860-            <awt.toolkit>com.github.caciocavallosilano.cacio.ctc.CTCToolkit</awt.toolkit>
1861-            <java.awt.headless>false</java.awt.headless>
--
2309-              </includes>
2310-              <excludes>
2311-                <!-- Skip auto-generated reports that have no authored links -->
2312:                <exclude>jacoco/**</exclude>
2313-                <exclude>xref/**</exclude>
2314-                <exclude>xref-test/**</exclude>
2315-                <exclude>dsm/**</exclude>
--
2508-        <spotbugs.skip>true</spotbugs.skip>
2509-        <xml.skip>true</xml.skip>
2510-        <forbiddenapis.skip>true</forbiddenapis.skip>
2511:        <jacoco.skip>true</jacoco.skip>
2512-        <maven.javadoc.skip>true</maven.javadoc.skip>
2513-        <linkcheck.skip>true</linkcheck.skip>
2514-        <jdepend.skip>true</jdepend.skip>
--
2533-    </profile>
2534-
2535-    <profile>
2536:      <!-- Profile for lychee offline mode (internal links only) -->
2537:      <id>lychee-offline</id>
2538-      <build>
2539-        <plugins>
2540-          <plugin>
--
2542-            <artifactId>lychee-maven-plugin</artifactId>
2543-            <configuration>
2544-              <args>
2545:                <arg>--offline</arg>
2546-                <arg>--config</arg>
2547-                <arg>${project.basedir}/config/lychee.toml</arg>
2548-                <arg>--root-dir</arg>
--
3298-    <profile>
3299-      <id>pitest-misc</id>
3300-      <properties>
3301:        <jacoco.skip>true</jacoco.skip>
3302-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
3303-      </properties>
3304-      <build>
--
3419-    <profile>
3420-      <id>pitest-annotation</id>
3421-      <properties>
3422:        <jacoco.skip>true</jacoco.skip>
3423-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
3424-      </properties>
3425-      <build>
--
3484-    <profile>
3485-      <id>pitest-blocks</id>
3486-      <properties>
3487:        <jacoco.skip>true</jacoco.skip>
3488-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
3489-      </properties>
3490-      <build>
--
3549-    <profile>
3550-      <id>pitest-coding-1</id>
3551-      <properties>
3552:        <jacoco.skip>true</jacoco.skip>
3553-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
3554-      </properties>
3555-      <build>
--
3687-    <profile>
3688-      <id>pitest-coding-2</id>
3689-      <properties>
3690:        <jacoco.skip>true</jacoco.skip>
3691-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
3692-      </properties>
3693-      <build>
--
3827-    <profile>
3828-      <id>pitest-coding-require-this-check</id>
3829-      <properties>
3830:        <jacoco.skip>true</jacoco.skip>
3831-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
3832-      </properties>
3833-      <build>
--
3889-    <profile>
3890-      <id>pitest-design</id>
3891-      <properties>
3892:        <jacoco.skip>true</jacoco.skip>
3893-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
3894-      </properties>
3895-      <build>
--
3951-    <profile>
3952-      <id>pitest-header</id>
3953-      <properties>
3954:        <jacoco.skip>true</jacoco.skip>
3955-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
3956-      </properties>
3957-      <build>
--
4013-    <profile>
4014-      <id>pitest-imports</id>
4015-      <properties>
4016:        <jacoco.skip>true</jacoco.skip>
4017-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
4018-      </properties>
4019-      <build>
--
4079-    <profile>
4080-      <id>pitest-indentation</id>
4081-      <properties>
4082:        <jacoco.skip>true</jacoco.skip>
4083-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
4084-      </properties>
4085-      <build>
--
4129-    <profile>
4130-      <id>pitest-javadoc</id>
4131-      <properties>
4132:        <jacoco.skip>true</jacoco.skip>
4133-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
4134-      </properties>
4135-      <build>
--
4204-    <profile>
4205-      <id>pitest-metrics</id>
4206-      <properties>
4207:        <jacoco.skip>true</jacoco.skip>
4208-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
4209-      </properties>
4210-      <build>
--
4266-    <profile>
4267-      <id>pitest-modifier</id>
4268-      <properties>
4269:        <jacoco.skip>true</jacoco.skip>
4270-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
4271-      </properties>
4272-      <build>
--
4331-    <profile>
4332-      <id>pitest-modules</id>
4333-      <properties>
4334:        <jacoco.skip>true</jacoco.skip>
4335-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
4336-      </properties>
4337-      <build>
--
4396-    <profile>
4397-      <id>pitest-naming</id>
4398-      <properties>
4399:        <jacoco.skip>true</jacoco.skip>
4400-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
4401-      </properties>
4402-      <build>
--
4461-    <profile>
4462-      <id>pitest-regexp</id>
4463-      <properties>
4464:        <jacoco.skip>true</jacoco.skip>
4465-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
4466-      </properties>
4467-      <build>
--
4523-    <profile>
4524-      <id>pitest-sizes</id>
4525-      <properties>
4526:        <jacoco.skip>true</jacoco.skip>
4527-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
4528-      </properties>
4529-      <build>
--
4585-    <profile>
4586-      <id>pitest-whitespace</id>
4587-      <properties>
4588:        <jacoco.skip>true</jacoco.skip>
4589-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
4590-      </properties>
4591-      <build>
--
4651-    <profile>
4652-      <id>pitest-ant</id>
4653-      <properties>
4654:        <jacoco.skip>true</jacoco.skip>
4655-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
4656-      </properties>
4657-      <build>
--
4717-    <profile>
4718-      <id>pitest-packagenamesloader</id>
4719-      <properties>
4720:        <jacoco.skip>true</jacoco.skip>
4721-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
4722-      </properties>
4723-      <build>
--
4776-    <profile>
4777-      <id>pitest-common</id>
4778-      <properties>
4779:        <jacoco.skip>true</jacoco.skip>
4780-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
4781-      </properties>
4782-      <build>
--
4916-    <profile>
4917-      <id>pitest-common-2</id>
4918-      <properties>
4919:        <jacoco.skip>true</jacoco.skip>
4920-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
4921-      </properties>
4922-      <build>
--
5005-    <profile>
5006-      <id>pitest-main</id>
5007-      <properties>
5008:        <jacoco.skip>true</jacoco.skip>
5009-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
5010-      </properties>
5011-      <build>
--
5069-    <profile>
5070-      <id>pitest-tree-walker</id>
5071-      <properties>
5072:        <jacoco.skip>true</jacoco.skip>
5073-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
5074-      </properties>
5075-      <build>
--
5188-    <profile>
5189-      <id>pitest-api</id>
5190-      <properties>
5191:        <jacoco.skip>true</jacoco.skip>
5192-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
5193-      </properties>
5194-      <build>
--
5277-    <profile>
5278-      <id>pitest-filters</id>
5279-      <properties>
5280:        <jacoco.skip>true</jacoco.skip>
5281-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
5282-      </properties>
5283-      <build>
--
5353-    <profile>
5354-      <id>pitest-utils</id>
5355-      <properties>
5356:        <jacoco.skip>true</jacoco.skip>
5357-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
5358-      </properties>
5359-      <build>
--
5537-    <profile>
5538-      <id>pitest-gui</id>
5539-      <properties>
5540:        <jacoco.skip>true</jacoco.skip>
5541-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
5542-      </properties>
5543-      <build>
--
5608-    <profile>
5609-      <id>pitest-xpath</id>
5610-      <properties>
5611:        <jacoco.skip>true</jacoco.skip>
5612-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
5613-      </properties>
5614-      <build>
--
5681-    <profile>
5682-      <id>pitest-java-ast-visitor</id>
5683-      <properties>
5684:        <jacoco.skip>true</jacoco.skip>
5685-        <checkstyle.skipCompileInputResources>true</checkstyle.skipCompileInputResources>
5686-      </properties>
5687-      <build>
subham@subham-Nitro-ANV15-41:~/checkstyle$ 
