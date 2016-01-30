# -*- coding: UTF-8 -*-
'''
Created on 2015年9月8日

@author: dxw
'''
from configFile import configFile
import time
from DDDProxy.hostParser import getDomainName
class domainConfig(configFile):
	defaultDomainList = ["google.com", "gstatic.com", "googleusercontent.com", "googleapis.com", "googleusercontent.com",
						"googlevideo.com", "facebook.com", "youtube.com", "akamaihd.net", "ytimg.com", "twitter.com",
						"feedly.com", "github.com", "wikipedia.org", "fbcdn.net", "blogspot.com", "t.co", "ggpht.com",
						"twimg.com", "facebook.net", "blogger.com", "flickr.com", "gmail.com", "stackoverflow.com",
						"gravatar.com", "gmail.com", "wikimedia.org", "v2ex.com", "blogspot.jp", "blogspot.com"]
	def __init__(self):
		configFile.__init__(self)
		if not self.setting:
			for domain in self.defaultDomainList:
				self.addDomain(domain)
			self.save()
	def getConfigfileFilePath(self):
		return configFile.makeConfigFilePathName("pacDomainConfig.json")

	def getDomainList(self, opend=1):
		"""
		0 close
		1 open 
		2 all
		"""
		pacList = []
		domainList = self.getDomainListWithAnalysis()
		for domain in domainList:
			if opend == 2 or domain["open"] == opend:
				pacList.append(domain["domain"])
		return pacList
	
	def getDomainListWithAnalysis(self):
		data = [{"domain":key, "open":value["open"], "connectTimes":value["connectTimes"]} for (key, value) in self.setting.items()]
		data.sort(cmp=lambda x, y : cmp(y["connectTimes"], x["connectTimes"]))
		return data;
	def removeDomain(self, domain):
		if domain in self.setting:
			del self.setting[domain]
			self.save()
			return True
		return False
	def closeDomain(self, domain):
		if domain in self.setting:
			self.setting[domain]["open"] = False
			self.save()
			return True
		return False
	def openDomain(self, domain):
		if domain in self.setting:
			self.setting[domain]["open"] = True
			self.save()
			return True
		return False
	def addDomain(self, domain, formGwflist=False, Open=True):
		if domain:
			if not domain in self.setting:
				self.setting[domain] = {"connectTimes":0, "open":Open, "formGwflist":formGwflist, "createTime":time.time()}
				self.save()
				return True
			else:
				currentDomain = self.setting[domain];
				if formGwflist:
					if currentDomain["connectTimes"] == 0 and currentDomain["formGwflist"] and time.time() - currentDomain["createTime"] > 3600 * 24 * 30:
						currentDomain["open"] = False
						self.save()
						return True
				else:
					currentDomain["open"] = Open
					self.save()
					return True
		return False
	def domainConnectTimes(self, domain, times):
		if domain in self.setting:
			data = self.setting[domain]
			data["connectTimes"] += times
			self.save()
		else:
			_domain = getDomainName(domain)
			if _domain and not _domain == domain:
				self.domainConnectTimes(_domain, times)
config = domainConfig()
