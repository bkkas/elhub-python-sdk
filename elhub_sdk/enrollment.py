"""
Processes related to the enrollment of customers
"""


def get_organization_meters(org_number: str) -> list:
    """
      https://dok.elhub.no/ediel200utkast/requestupfrontmeteringpointcharacteristics

    Query Endpoint

    <wsdl:message name="RequestUpfrontMeteringPointCharacteristicsRequest">
      <wsdl:part name="RequestUpfrontMeteringPointCharacteristicsRequest" element="tns:RequestUpfrontMeteringPointCharacteristicsRequest"></wsdl:part>


      <xsd:element name="ConsumerInvolvedCustomerParty" type="abie:Elhub_EndUserIdentificationType" minOccurs="0" maxOccurs="1"/>

          < xsd: complexType    name = "Elhub_EndUserIdentificationType" >
              < xsd: sequence >    < xsd: element    name = "Identification"    type = "bdt:Elhub_EndUserIdentifierType"    minOccurs = "1"    maxOccurs = "1" / >
          < / xsd: sequence >< / xsd: complexType >

            <xsd:complexType name="Elhub_EndUserIdentifierType">
              <xsd:simpleContent>
                <xsd:extension base="bdt:String11Type">
                  <xsd:attribute name="schemeAgencyIdentifier" use="required" type="bdt:Elhub_schemeAgencyIdentifierType"/>
                </xsd:extension>
              </xsd:simpleContent>
            </xsd:complexType>

                <xsd:simpleType name="Elhub_schemeAgencyIdentifierType">
                  <xsd:restriction base="xsd:string">
                    <xsd:enumeration value="82"/> -> organization number
                    <xsd:enumeration value="Z01"/> -> SS number
                  </xsd:restriction>
                </xsd:simpleType>


      <xsd:element name="MPAddressMeteringPointAddress" type="abie:Elhub_MPAddressSearchType" minOccurs="0" maxOccurs="1"/>
      <xsd:element name="MeteringInstallationMeterFacility" type="abie:Elhub_MeterSearchType" minOccurs="0" maxOccurs="1"/>
    """
