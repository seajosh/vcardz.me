import pickle
import pymongo
import sys

import xml.etree.ElementTree as tree


# temp until I get the vcard code packaged up
sys.path.insert(0, '../src/lib/')

from kontexa.google import GoogleFeed


bad_xml_1 = """<?xml version="1.0" encoding="UTF-8"?>
<feed gd:etag="&quot;QHs-cDVSLyt7I2A9XRRSFkwCRwI.&quot;" xmlns="http://www.w3.org/2005/Atom" xmlns:batch="http://schemas.google.com/gdata/batch" xmlns:gContact="http://schemas.google.com/contact/2008" xmlns:gd="http://schemas.google.com/g/2005" xmlns:openSearch="http://a9.com/-/spec/opensearch/1.1/">
 <id>josh.watts@gmail.com</id>
 <updated>2015-01-18T21:54:21.558Z</updated>
 <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
 <title>Josh Watts's Contacts</title>
 <link rel="alternate" type="text/html" href="https://www.google.com/"/>
 <link rel="http://schemas.google.com/g/2005#feed" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full"/>
 <link rel="http://schemas.google.com/g/2005#post" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full"/>
 <link rel="http://schemas.google.com/g/2005#batch" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/batch"/>
 <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full?max-results=25"/>
 <link rel="next" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full?max-results=25&amp;start-index=26"/>
 <author>
  <name>Josh Watts</name>
  <email>josh.watts@gmail.com</email>
 </author>
 <generator version="1.0" uri="http://www.google.com/m8/feeds">Contacts</generator>
 <openSearch:totalResults>1121</openSearch:totalResults>
 <openSearch:startIndex>1</openSearch:startIndex>
 <openSearch:itemsPerPage>25</openSearch:itemsPerPage>
 <entry gd:etag="&quot;Qno6ezRQKCt7I2A9XRRSEEoCRgE.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/1</id>
  <updated>2015-01-12T15:55:53.413Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2015-01-12T15:55:53.413Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Andy Emerson</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/1"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/1"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/1"/>
  <gd:name>
   <gd:fullName_xxx>Andy Emerson</gd:fullName_xxx>
   <gd:givenName>Andy</gd:givenName>
   <gd:familyName>Emerson</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#work" address="aemerson@conveyorengineering.com" primary="true"/>
  <gd:email rel="http://schemas.google.com/g/2005#home" address="andymrsn@gmail.com"/>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#mobile" uri="tel:+1-208-412-9177">2084129177</gd:phoneNumber>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#home" uri="tel:+1-208-338-5216">208-338-5216</gd:phoneNumber>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/270f"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/3eed73d78f055389"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/6"/>
 </entry>
</feed>"""

bad_xml_2 = """<?xml version="1.0" encoding="UTF-8"?>
<feed gd:etag="&quot;QHs-cDVSLyt7I2A9XRRSFkwCRwI.&quot;" xmlns="http://www.w3.org/2005/Atom" xmlns:batch="http://schemas.google.com/gdata/batch" xmlns:gContact="http://schemas.google.com/contact/2008" xmlns:gd="http://schemas.google.com/g/2005" xmlns:openSearch="http://a9.com/-/spec/opensearch/1.1/">
 <id>josh.watts@gmail.com</id>
 <updated>2015-01-18T21:54:21.558Z</updated>
 <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
 <title>Josh Watts's Contacts</title>
 <link rel="alternate" type="text/html" href="https://www.google.com/"/>
 <link rel="http://schemas.google.com/g/2005#feed" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full"/>
 <link rel="http://schemas.google.com/g/2005#post" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full"/>
 <link rel="http://schemas.google.com/g/2005#batch" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/batch"/>
 <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full?max-results=25"/>
 <link rel="next" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full?max-results=25&amp;start-index=26"/>
 <author>
  <name>Josh Watts</name>
  <email>josh.watts@gmail.com</email>
 </author>
 <generator version="1.0" uri="http://www.google.com/m8/feeds">Contacts</generator>
 <openSearch:totalResults>1121</openSearch:totalResults>
 <openSearch:startIndex>1</openSearch:startIndex>
 <openSearch:itemsPerPage>25</openSearch:itemsPerPage>
 <entry gd:etag="&quot;Qno6ezRQKCt7I2A9XRRSEEoCRgE.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/1</id>
  <updated>2015-01-12T15:55:53.413Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2015-01-12T15:55:53.413Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Andy Emerson</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/1"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/1"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/1"/>
  <gd:name_xxx>
   <gd:fullName_xxx>Andy Emerson</gd:fullName_xxx>
   <gd:givenName>Andy</gd:givenName>
   <gd:familyName>Emerson</gd:familyName>
  </gd:name_xxx>
  <gd:email rel="http://schemas.google.com/g/2005#work" address="aemerson@conveyorengineering.com" primary="true"/>
  <gd:email rel="http://schemas.google.com/g/2005#home" address="andymrsn@gmail.com"/>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#mobile" uri="tel:+1-208-412-9177">2084129177</gd:phoneNumber>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#home" uri="tel:+1-208-338-5216">208-338-5216</gd:phoneNumber>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/270f"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/3eed73d78f055389"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/6"/>
 </entry>
</feed>"""

xml = """<?xml version="1.0" encoding="UTF-8"?>
<feed gd:etag="&quot;QHs-cDVSLyt7I2A9XRRSFkwCRwI.&quot;" xmlns="http://www.w3.org/2005/Atom" xmlns:batch="http://schemas.google.com/gdata/batch" xmlns:gContact="http://schemas.google.com/contact/2008" xmlns:gd="http://schemas.google.com/g/2005" xmlns:openSearch="http://a9.com/-/spec/opensearch/1.1/">
 <id>josh.watts@gmail.com</id>
 <updated>2015-01-18T21:54:21.558Z</updated>
 <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
 <title>Josh Watts's Contacts</title>
 <link rel="alternate" type="text/html" href="https://www.google.com/"/>
 <link rel="http://schemas.google.com/g/2005#feed" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full"/>
 <link rel="http://schemas.google.com/g/2005#post" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full"/>
 <link rel="http://schemas.google.com/g/2005#batch" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/batch"/>
 <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full?max-results=25"/>
 <link rel="next" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full?max-results=25&amp;start-index=26"/>
 <author>
  <name>Josh Watts</name>
  <email>josh.watts@gmail.com</email>
 </author>
 <generator version="1.0" uri="http://www.google.com/m8/feeds">Contacts</generator>
 <openSearch:totalResults>1121</openSearch:totalResults>
 <openSearch:startIndex>1</openSearch:startIndex>
 <openSearch:itemsPerPage>25</openSearch:itemsPerPage>
 <entry gd:etag="&quot;Qno6ezRQKCt7I2A9XRRSEEoCRgE.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/1</id>
  <updated>2015-01-12T15:55:53.413Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2015-01-12T15:55:53.413Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Andy Emerson</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/1"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/1"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/1"/>
  <gd:name>
   <gd:fullName>Andy Emerson</gd:fullName>
   <gd:givenName>Andy</gd:givenName>
   <gd:familyName>Emerson</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#work" address="aemerson@conveyorengineering.com" primary="true"/>
  <gd:email rel="http://schemas.google.com/g/2005#home" address="andymrsn@gmail.com"/>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#mobile" uri="tel:+1-208-412-9177">2084129177</gd:phoneNumber>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#home" uri="tel:+1-208-338-5216">208-338-5216</gd:phoneNumber>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/270f"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/3eed73d78f055389"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/6"/>
 </entry>
 <entry gd:etag="&quot;Qno6ezRQKCt7I2A9XRRSEEoCRgE.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/2</id>
  <updated>2015-01-12T15:55:53.413Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2015-01-12T15:55:53.413Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Brian Chinn</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/2"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/2"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/2"/>
  <gd:name>
   <gd:fullName>Brian Chinn</gd:fullName>
   <gd:givenName>Brian</gd:givenName>
   <gd:familyName>Chinn</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="bchinn@jmaarch.com" primary="true"/>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#mobile" uri="tel:+1-702-249-1632">7022491632</gd:phoneNumber>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#work" uri="tel:+1-702-731-2033">7027312033</gd:phoneNumber>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/270f"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/6"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/3eed73d78f055389"/>
 </entry>
 <entry gd:etag="&quot;SXc-fzVSLit7I2A9WhFSGEoOQAI.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/3</id>
  <updated>2013-06-22T04:19:28.957Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2013-06-22T04:19:28.957Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Brad DesAulniers</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/3"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/3"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/3"/>
  <gd:name>
   <gd:fullName>Brad DesAulniers</gd:fullName>
   <gd:givenName>Brad</gd:givenName>
   <gd:familyName>DesAulniers</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="bradd@us.ibm.com" primary="true"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/270f"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/6"/>
 </entry>
 <entry gd:etag="&quot;R3g_ejVSLit7I2A9XRdREEQMRQE.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/4</id>
  <updated>2014-09-30T16:57:36.642Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2014-09-30T16:57:36.642Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Craig Crowley</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/4"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/4"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/4"/>
  <gd:name>
   <gd:fullName>Craig Crowley</gd:fullName>
   <gd:givenName>Craig</gd:givenName>
   <gd:familyName>Crowley</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="ccrowley@dci-engineers.com" primary="true"/>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#mobile" uri="tel:+1-509-998-3568">+15099983568</gd:phoneNumber>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/270f"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/3eed73d78f055389"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/6"/>
 </entry>
 <entry gd:etag="&quot;SXY7fTVSLyt7I2A9WxFaF04MQgc.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/6</id>
  <updated>2010-07-21T18:22:18.805Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2010-07-21T18:22:18.805Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Denver Passow</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/6"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/6"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/6"/>
  <gd:name>
   <gd:fullName>Denver Passow</gd:fullName>
   <gd:givenName>Denver</gd:givenName>
   <gd:familyName>Passow</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="denverpassow@hotmail.com" primary="true"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/270f"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/3eed73d78f055389"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/6"/>
 </entry>
 <entry gd:etag="&quot;Qno6ezRQKCt7I2A9XRRSEEoCRgE.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/7</id>
  <updated>2015-01-12T15:55:53.413Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2015-01-12T15:55:53.413Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>John Deverall</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/7"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/7"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/7"/>
  <gd:name>
   <gd:fullName>John Deverall</gd:fullName>
   <gd:givenName>John</gd:givenName>
   <gd:familyName>Deverall</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="devjp@hotmail.com" primary="true"/>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#mobile" uri="tel:+1-208-863-6850">(208) 863-6850</gd:phoneNumber>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/270f"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/3eed73d78f055389"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/6"/>
 </entry>
 <entry gd:etag="&quot;Q38zfjVSLit7I2A9WhJXFE4MQAc.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/8</id>
  <updated>2012-08-08T14:38:52.186Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2012-08-08T14:38:52.186Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>David Giordano</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/8"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/8"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/8"/>
  <gd:name>
   <gd:fullName>David Giordano</gd:fullName>
   <gd:givenName>David</gd:givenName>
   <gd:familyName>Giordano</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="dgiordano@dci-engineers.com" primary="true"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/270f"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/6"/>
 </entry>
 <entry gd:etag="&quot;Q38zfjVSLit7I2A9WhJXFE4MQAc.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/9</id>
  <updated>2012-08-08T14:38:52.186Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2012-08-08T14:38:52.186Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Dustan Bott</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/9"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/9"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/9"/>
  <gd:name>
   <gd:fullName>Dustan Bott</gd:fullName>
   <gd:givenName>Dustan</gd:givenName>
   <gd:familyName>Bott</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="dustanbott@hotmail.com" primary="true"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/270f"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/3eed73d78f055389"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/6"/>
 </entry>
 <entry gd:etag="&quot;Q38zfjVSLit7I2A9WhJXFE4MQAc.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/a</id>
  <updated>2012-08-08T14:38:52.186Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2012-08-08T14:38:52.186Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title/>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/a"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/a"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/a"/>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="endofauction@ebay.com" primary="true"/>
 </entry>
 <entry gd:etag="&quot;R3g_fDVSLit7I2A9WhRVE04JRAI.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/b</id>
  <updated>2012-01-12T01:56:06.644Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2012-01-12T01:56:06.644Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Jefferson Jenkins</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/b"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/b"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/b"/>
  <gd:name>
   <gd:fullName>Jefferson Jenkins</gd:fullName>
   <gd:givenName>Jefferson</gd:givenName>
   <gd:familyName>Jenkins</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="jjenkins6@yahoo.com" primary="true"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/270f"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/3eed73d78f055389"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/6"/>
 </entry>
 <entry gd:etag="&quot;SX44fzVSLit7I2A9XRdQFUsDQQY.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/d</id>
  <updated>2014-10-17T18:13:48.037Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2014-10-17T18:13:48.037Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Kevin Henry</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/d"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/d"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/d"/>
  <gd:name>
   <gd:fullName>Kevin Henry</gd:fullName>
   <gd:givenName>Kevin</gd:givenName>
   <gd:familyName>Henry</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="kevinandsunday@msn.com" primary="true"/>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="vandalmd@live.com"/>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#mobile" uri="tel:+1-208-859-8950">(208) 859-8950</gd:phoneNumber>
  <gd:structuredPostalAddress rel="http://schemas.google.com/g/2005#home">
   <gd:formattedAddress>304 E 7th St.
Moscow, ID 83843
United States of America</gd:formattedAddress>
   <gd:street>304 E 7th St.</gd:street>
   <gd:city>Moscow</gd:city>
   <gd:region>ID</gd:region>
   <gd:postcode>83843</gd:postcode>
   <gd:country>United States of America</gd:country>
  </gd:structuredPostalAddress>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/270f"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/3eed73d78f055389"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/6"/>
 </entry>
 <entry gd:etag="&quot;Q38zfjVSLit7I2A9WhJXFE4MQAc.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/e</id>
  <updated>2012-08-08T14:38:52.186Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2012-08-08T14:38:52.186Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title/>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/e"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/e"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/e"/>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="loanhelp@roadloans.com" primary="true"/>
 </entry>
 <entry gd:etag="&quot;Qno6ezRQKCt7I2A9XRRSEEoCRgE.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/f</id>
  <updated>2015-01-12T15:55:53.413Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2015-01-12T15:55:53.413Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Lou Mallane</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/f"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/f"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/f"/>
  <gd:name>
   <gd:fullName>Lou Mallane</gd:fullName>
   <gd:givenName>Lou</gd:givenName>
   <gd:familyName>Mallane</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="lou@louiespizza.com" primary="true"/>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#mobile" uri="tel:+1-208-841-2702">2088412702</gd:phoneNumber>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/270f"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/3eed73d78f055389"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/6"/>
 </entry>
 <entry gd:etag="&quot;Qno6ezRQKCt7I2A9XRRSEEoCRgE.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/10</id>
  <updated>2015-01-12T15:55:53.413Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2015-01-12T15:55:53.413Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Luke Wallace</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/10"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/10"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/10"/>
  <gd:name>
   <gd:fullName>Luke Wallace</gd:fullName>
   <gd:givenName>Luke</gd:givenName>
   <gd:familyName>Wallace</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="luke_wallace@hotmail.com" primary="true"/>
  <gd:email rel="http://schemas.google.com/g/2005#home" address="luke_wallace@hotmail.com"/>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="luke@thedesignsyndicate.com"/>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#mobile" uri="tel:+1-206-501-7330">206.501.7330</gd:phoneNumber>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#work" uri="tel:+1-206-685-6463">2066856463</gd:phoneNumber>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/270f"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/3eed73d78f055389"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/6"/>
 </entry>
 <entry gd:etag="&quot;Q3oyezVSLyt7I2A9WxZbE0sNRww.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/11</id>
  <updated>2008-04-16T17:31:22.493Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2008-04-16T17:31:22.493Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title/>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/11"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/11"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/11"/>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="me@gmail.com" primary="true"/>
 </entry>
 <entry gd:etag="&quot;Q38zfjVSLit7I2A9WhJXFE4MQAc.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/12</id>
  <updated>2012-08-08T14:38:52.186Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2012-08-08T14:38:52.186Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Mike Vance</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/12"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/12"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/12"/>
  <gd:name>
   <gd:fullName>Mike Vance</gd:fullName>
   <gd:givenName>Mike</gd:givenName>
   <gd:familyName>Vance</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="michael.vance@americanmedicalsystems.com" primary="true"/>
 </entry>
 <entry gd:etag="&quot;Qno6ezRQKCt7I2A9XRRSEEoCRgE.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/13</id>
  <updated>2015-01-12T15:55:53.413Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2015-01-12T15:55:53.413Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Nick Osloond</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/13"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/13"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/13"/>
  <gd:name>
   <gd:fullName>Nick Osloond</gd:fullName>
   <gd:givenName>Nick</gd:givenName>
   <gd:familyName>Osloond</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="mogrotto@hotmail.com" primary="true"/>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#mobile" uri="tel:+1-208-870-9916">2088709916</gd:phoneNumber>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/270f"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/3eed73d78f055389"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/6"/>
 </entry>
 <entry gd:etag="&quot;Q38zfjVSLit7I2A9WhJXFE4MQAc.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/14</id>
  <updated>2012-08-08T14:38:52.186Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2012-08-08T14:38:52.186Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title/>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/14"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/14"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/14"/>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="opinionjournal@wsj.com" primary="true"/>
 </entry>
 <entry gd:etag="&quot;Q38zfjVSLit7I2A9WhJXFE4MQAc.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/15</id>
  <updated>2012-08-08T14:38:52.186Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2012-08-08T14:38:52.186Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Ryan Carnie</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/15"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/15"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/15"/>
  <gd:name>
   <gd:fullName>Ryan Carnie</gd:fullName>
   <gd:givenName>Ryan</gd:givenName>
   <gd:familyName>Carnie</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="rcarnie1369@hotmail.com" primary="true"/>
 </entry>
 <entry gd:etag="&quot;Qno6ezRQKCt7I2A9XRRSEEoCRgE.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/16</id>
  <updated>2015-01-12T15:55:53.413Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2015-01-12T15:55:53.413Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>David Schorch</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/16"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/16"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/16"/>
  <gd:name>
   <gd:fullName>David Schorch</gd:fullName>
   <gd:givenName>David</gd:givenName>
   <gd:familyName>Schorch</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="rosump@comcast.net" primary="true"/>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#mobile" uri="tel:+1-770-330-7162">770.330.7162</gd:phoneNumber>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#home" uri="tel:+1-678-352-7870">6783527870</gd:phoneNumber>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/6"/>
 </entry>
 <entry gd:etag="&quot;Rn85ejVSLyt7I2A9WxBXEU0OTwc.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/17</id>
  <updated>2010-01-21T20:13:57.122Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2010-01-21T20:13:57.122Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Richard Reichner</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/17"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/17"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/17"/>
  <gd:name>
   <gd:fullName>Richard Reichner</gd:fullName>
   <gd:givenName>Richard</gd:givenName>
   <gd:familyName>Reichner</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="rr@sciatlanta.com" primary="true"/>
 </entry>
 <entry gd:etag="&quot;Qno6ezRQKCt7I2A9XRRSEEoCRgE.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/18</id>
  <updated>2015-01-12T15:55:53.413Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2015-01-12T15:55:53.413Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Andy Watts</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/18"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/18"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/18"/>
  <gd:name>
   <gd:fullName>Andy Watts</gd:fullName>
   <gd:givenName>Andy</gd:givenName>
   <gd:familyName>Watts</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="rynedee@runbox.com" primary="true"/>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#mobile" uri="tel:+1-208-602-6433">(208) 602-6433</gd:phoneNumber>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/2710"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/3eed73d78f055389"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/6"/>
 </entry>
 <entry gd:etag="&quot;Qno6ezRQKCt7I2A9XRRSEEoCRgE.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/1b</id>
  <updated>2015-01-12T15:55:53.413Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2015-01-12T15:55:53.413Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Katie Hagadone</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/1b"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/1b"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/1b"/>
  <gd:name>
   <gd:fullName>Katie Hagadone</gd:fullName>
   <gd:givenName>Katie</gd:givenName>
   <gd:familyName>Hagadone</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="katiehagadone@live.com" primary="true"/>
  <gd:phoneNumber rel="http://schemas.google.com/g/2005#mobile" uri="tel:+1-208-863-3550">208-863-3550</gd:phoneNumber>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/2710"/>
  <gContact:groupMembershipInfo deleted="false" href="http://www.google.com/m8/feeds/groups/josh.watts%40gmail.com/base/6"/>
 </entry>
 <entry gd:etag="&quot;Q38zfjVSLit7I2A9WhJXFE4MQAc.&quot;">
  <id>http://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/base/1f</id>
  <updated>2012-08-08T14:38:52.186Z</updated>
  <app:edited xmlns:app="http://www.w3.org/2007/app">2012-08-08T14:38:52.186Z</app:edited>
  <category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/contact/2008#contact"/>
  <title>Jason McMunn</title>
  <link rel="http://schemas.google.com/contacts/2008/rel#photo" type="image/*" href="https://www.google.com/m8/feeds/photos/media/josh.watts%40gmail.com/1f" gd:etag="&quot;c2V8H2QGSit7I2A_GWMXdSJuJ241OmgQMCY.&quot;"/>
  <link rel="self" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/1f"/>
  <link rel="edit" type="application/atom+xml" href="https://www.google.com/m8/feeds/contacts/josh.watts%40gmail.com/full/1f"/>
  <gd:name>
   <gd:fullName>Jason McMunn</gd:fullName>
   <gd:givenName>Jason</gd:givenName>
   <gd:familyName>McMunn</gd:familyName>
  </gd:name>
  <gd:email rel="http://schemas.google.com/g/2005#other" address="mcmunn@mcmunn.com" primary="true"/>
 </entry>
</feed>"""

ATOM_NS = 'http://www.w3.org/2005/Atom'

def wrap_ns(elem, ns):
    return '{%s}%s' % (ns, elem)



# tree.register_namespace('','http://www.w3.org/2005/Atom')
# root = tree.fromstring(xml)
# for child in root:
#     print(child.tag)
# for entry in root.iter('{http://www.w3.org/2005/Atom}entry'):
#     print(entry.find(wrap_ns('title', ATOM_NS)).text)

google = GoogleFeed(xml)
for card in google:
    print(card)


# root = feedparser.parse(xml)
# entryIter = iter(root.entries)
# entry = next(entryIter)
# print(entry.title)
# entry = next(entryIter)
# print(entry.title)


